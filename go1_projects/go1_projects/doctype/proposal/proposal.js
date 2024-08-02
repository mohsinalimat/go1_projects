// Copyright (c) 2018, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Proposal', {
	refresh: function (frm) {
		if(frm.doc.count == 0){
			frm.add_custom_button(__("Send Mail"), function(){
				frappe.prompt([{
					'fieldname': 'subject',
					'fieldtype': 'Data',
					'label': __('Subject'),
					'reqd': 1
				},
				{
					'fieldname': 'email_content',
					'fieldtype': 'Text Editor',
					'label': __('Email Content'),
					'reqd': 1
				}],
				function(values){
					console.log(values)
					frappe.call({
						method: "go1_projects.go1_projects.doctype.proposal.proposal.sendproposalemail",
						args: {
							route: window.location.origin+'/'+frm.doc.route,
							title: values.subject,
							body: values.email_content,
							email: frm.doc.client_email,
							cname: frm.doc.client_name,
							cover: frm.doc.title,
						},
						callback: function(r) {
								frm.set_value("subject", values.subject);
								console.log(r.message)
								var freq = r.message;
								var count = frm.doc.count + 1;
								frm.set_value("count", count)
								var t = frappe.datetime.get_today();
								frm.set_value("first_notification_date", t);
								refresh_field("first_notification_date");
								frm.set_value("second_notification_date", frappe.datetime.add_days(frappe.datetime.get_today(), freq*1));
								frm.set_value("third_notification_date", frappe.datetime.add_days(frappe.datetime.get_today(), freq*2));
								frm.set_value("fourth_notification_date", frappe.datetime.add_days(frappe.datetime.get_today(), freq*3));							
								refresh_field("count");
								frm.save();
							}
					});				
				},
				__('Email Details'))
			});
		}
		else if(frm.doc.count > 0){
			frm.add_custom_button(__("Time Sheet"), function(){

				frappe.call({
					method: "go1_projects.go1_projects.controller.senddailytimesheet",
					args: {},
					callback: function(r) {
							console.log(r.message)
						}
				});			
			});
		}
	},
	validate: function (frm) {
		frm.set_value('date', frappe.datetime.get_today());
		var total = 0;
		for(var i in frm.doc.items){
			total += frm.doc.items[i].rate
		}
		frm.set_value("sub_total",total);
		frm.set_value('tax', frm.doc.sub_total*18/100);
		frm.set_value('grand_total', frm.doc.sub_total + frm.doc.tax)
		// body...
	},
	lead: function (frm) {
		if(frm.doc.lead){
			frappe.call({
				method: "go1_projects.go1_projects.doctype.proposal.proposal.get_lead_details",
				args: {
					lead: frm.doc.lead,
				},
				async: false,
				callback: function(r) {
					console.log(r.message)
					frm.set_value('client_name', r.message.lead_name)
					frm.set_value('client_contact_no', r.message.mobile_no)
					frm.set_value('client_email', r.message.email_id)

					}
			});
		}	
				
	},
	sub_total: function(frm) {
		frm.set_value('tax', frm.doc.sub_total*18/100);
	},
	tax: function(frm) {
		frm.set_value('grand_total', frm.doc.sub_total + frm.doc.tax)
	},
	product: function(frm) {
		if (frm.doc.product && !frm.doc.currency) {
			frm.set_value('product', null)
			frappe.throw("Please Select a currency.")

		}
		if(frm.doc.product && frm.doc.currency){
			frappe.call({
				method: "go1_projects.go1_projects.doctype.proposal.proposal.get_data_from_template",
				args: {
					template: frm.doc.product,
				},
				callback: function(r) {
					$.each(r.message[0], function(i, d) {
						var row = frappe.model.add_child(frm.doc, "Proposal Data", "contents");
						
						row.title = d.title
						row.content = d.content

					});
			 		refresh_field("contents");
					$.each(r.message[1], function(i, d) {
						var row = frappe.model.add_child(frm.doc, "Proposal Samples", "samples");
						
						row.image = d.image
						row.url = d.url

					});
			 		refresh_field("samples");

							}
			});

			frappe.call({
				method: "go1_projects.go1_projects.doctype.proposal.proposal.get_items_from_template",
				args: {
					currency: frm.doc.currency,
					template: frm.doc.product,
				},
				async: false,
				callback: function(r) {
					// console.log(r.message)
					$.each(r.message, function(i, d) {
						var row = frappe.model.add_child(frm.doc, "Proposal Child", "items");
						
						row.rate = d.rate
						row.qty = d.qty
						row.price = d.price
						row.item = d.item
						row.description = d.description
						row.currency = d.currency

					});
			 		refresh_field("items");

					}
			});

			console.log(frm.doc.items)
		}

	},
	currency: function (frm) {
		var current_currency = frm.doc.currency
		
		frappe.call({
			method: 'frappe.client.get_value',
			args: {
				doctype: "Currency",
				filters: {"name": frm.doc.currency},
				fieldname: "symbol"
			},
			callback: function(r){
				if(r.message){
					frm.set_value('symbol',r.message.symbol)
					frm.set_currency_labels(["sub_total", "tax", "grand_total", "price"], current_currency);
					// var row = frappe.model.add_child(frm.doc, "Proposal Child", "items");
				}
			}
		})
		console.log(frm.doc.items)


		
		if(frm.doc.product){
			frappe.call({
				method: "go1_projects.go1_projects.doctype.proposal.proposal.get_items_from_template",
				args: {
					template: frm.doc.product,
					currency: frm.doc.currency
				},
				async: false,
				callback: function(r) {
					// console.log(r.message)
					for(var j in frm.doc.items){
						frm.get_field("items").grid.grid_rows[j].remove();	
					}
					$.each(r.message, function(i, d) {
						var row = frappe.model.add_child(frm.doc, "Proposal Child", "items");
						
						row.rate = d.rate
						row.qty = d.qty
						row.price = d.price
						row.item = d.item
						row.description = d.description
						row.currency = d.currency

					});
			 		refresh_field("items");

					}
			});
		}

	}
});

 
	

frappe.ui.form.on("Proposal Child", "rate", function multiply_quantity(frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	var total = 0;
	for(var i in frm.doc.items){
		total += frm.doc.items[i].rate
	}
	frm.set_value("sub_total",total);
});   
	
frappe.ui.form.on("Proposal Child", "qty", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "rate", d.qty * d.price);

}); 	

frappe.ui.form.on("Proposal Child", "price", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "rate", d.qty * d.price);

});