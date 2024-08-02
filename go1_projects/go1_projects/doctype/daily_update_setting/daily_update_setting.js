// Copyright (c) 2024, info@tridotstech.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Update Setting', {
	refresh: function(frm) {
		frm.add_custom_button("Morning Update",function(){
				frappe.call({
					method:"go1_projects.api.cumulative_update_message",
					callback(r){
						frappe.msgprint("Morning update report scheduled successfully")
					}
				})
		},__("Send Mail"));

		frm.add_custom_button("Closing Update",function(){
			frappe.call({
				method:"go1_projects.api.cumulative_closing_update",
				callback(r){
					frappe.msgprint("Closing update scheduled successfully")
				}
			})
		},__("Send Mail"));

		frm.add_custom_button("Reporting To",function(){
			frappe.call({
				method:"go1_projects.api.mail_reports_to",
				callback(r){
					frappe.msgprint("Reporting to update scheduled successfully")
				}
			})
		},__("Send Mail"))
		frm.add_custom_button("Project Wise Report",function(){
			frappe.call({
				method:"go1_projects.api.project_wise_tracking",
				callback(r){
					
				}
			})
		})
		
	},
	report_mail(frm){
		if(frm.doc.reports_to){
			frappe.call({
				method:"go1_projects.api.mail_reports_to",
			})
		}
	}


});
