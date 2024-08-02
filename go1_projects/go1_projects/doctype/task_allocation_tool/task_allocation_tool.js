// Copyright (c) 2024, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on("Task Allocation Tool", {
	refresh: function (frm) {
		frm.disable_save()
		frm.add_custom_button("Assign", function () {
			frappe.call({
				doc: frm.doc,
				method: "assign_tasks_enqueue",
				args: {
					"json": frm.doc
				},
				async: false,
				callback(r) {
					if (r.message) {
						frm.set_value("project", "")
						frm.set_value("task", "")
						frappe.msgprint("Assign tasks scheduled")
						// setTimeout(function () {
						// 	frm.save();
						// }, 1000)
					}
				}
			})
		})
		frappe.call({
			doc: frm.doc,
			method: 'get_allocation_history',
			async: false,
			callback: function (r) {
				if (r.message) {
					// console.log(r.message)
					// console.log(typeof(r.message))
					if(r.message.length > 0){
						let cards = []
						let val = 0
						let table_data = ""
						for (let i of r.message) {
							let card_data = ""
							let data = ""
							let start = ""
							start=`<div id="collapse${val}" class="collapse" >
								<div class="card-body">`
							for(let j of i.tasks){
								data += `<div style="border:1px solid #c0c6cc; margin-bottom:10px;border-radius:10px;display:flex;justify-content:space-around;align-items:center;">
									<p style = "margin:0;text-align:center;flex:1;">${j.proj}</p>
									<p style="margin:0;text-align:center;flex:1;">${j.task}</p>
									<p style="margin:0;text-align:center;flex:1;">${j.desc}</p>
									<p style="margin:0;text-align:center;flex:1;padding: 10px;">${j.status}</p>
								</div>`
						
							}
							val++
							card_data = start+data+`</div></div>`
							cards.push(card_data)
						}
						val = 0
						for (let [index,i] of r.message.entries()) {
							table_data += `<div class="card" style="margin-bottom:10px;"> 
								<div class="card-header" style='border-bottom:none;'>
									<h5 class="mb-0">
										<i class="fa fa-angle-right"></i>
										<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse${val}" >
										${i.name}
										</button>
									</h5>
								</div>
								${cards[index]}
							</div>`
							val++
						}
	
						//TABLE
						// let formatted_html = `<table style="width:100%;border:1px solid #c6cdd3;border-collapse: collapse;">
						// <tr>
						// 	<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center; padding:10px;">Project</th>
						// 	<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center; padding:10px;">Project Name</th>
						// 	<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center; padding:10px;">Task</th>
						// 	<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center;padding:10px;">Status</th>
						// 	<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center;padding:10px;">Description</th>
						// </tr>
						// ${table_data}
						// </table>`
						// console.log(table_data)
						// console.log(formatted_html)
						// frm.set_value("dashboard",formatted_html)
						frm.set_df_property("dashboard", "options", table_data)
						frm.refresh_field("dashboard")
						$(document).on('show.bs.collapse', '.collapse', function () {
							$(this).prev('.card-header').find('.fa.fa-angle-right').removeClass('fa-angle-right').addClass('fa-angle-down');
						});
						
						$(document).on('hide.bs.collapse','.collapse',function(){
							$(this).prev('.card-header').find('.fa.fa-angle-down').removeClass('fa-angle-down').addClass('fa-angle-right');
				
						})        
					}else{
						let dummy_data = `<div style="min-height:350px;display:flex;align-items:center;justify-content:center;"><h5><i class="fa fa-history" style="font-size:18px;"></i> No Allocation History Found....</h5></div>`
						frm.set_df_property("dashboard", "options", dummy_data)
						frm.refresh_field("dashboard")
					}
				}
			}
		})
		// if(frm.doc.history_json){
		// 	let table_data = ``
		// 	if(frm.doc.history_json != "[]"){
		// 		console.log(frm.doc.history_json)
		// 		for(let i of JSON.parse(frm.doc.history_json)){
		// 			table_data+=`<tr>
		// 			<td style="border:1px solid #c6cdd3; padding:8px;border-collapse: collapse; text-align:center;">${i.proj}</td>
		// 			<td style="border:1px solid #c6cdd3; padding:8px;border-collapse: collapse; text-align:center;">${i.proj_name}</td>
		// 			<td style="border:1px solid #c6cdd3; padding:8px;border-collapse: collapse; text-align:center;">${i.reference_name}</td>
		// 			<td style="border:1px solid #c6cdd3; padding:8px; border-collapse: collapse; text-align:center;">${i.status}</td>
		// 			<td style="border:1px solid #c6cdd3;padding:8px; border-collapse: collapse; text-align:center;">${i.description}</td>
		// 			</tr>`
		// 		}
		// 	}else{
		// 		table_data+=`
		// 		<tr>
		// 			<td style="border:1px solid #c6cdd3;padding:8px; border-collapse: collapse; text-align:center;" colspan="5">No Allocation history...</td>
		// 		</tr>
		// 		`
		// 	}
		// 	let formatted_html = `<table style="width:100%;border:1px solid #c6cdd3;border-collapse: collapse;">
		// 	<tr>
		// 		<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center; padding:10px;">Project</th>
		// 		<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center; padding:10px;">Project Name</th>
		// 		<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center; padding:10px;">Task</th>
		// 		<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center;padding:10px;">Status</th>
		// 		<th style="border:1px solid #c6cdd3;border-collapse: collapse; text-align:center;padding:10px;">Description</th>
		// 	</tr>
		// 	${table_data}
		// 	</table>`
		// 	// console.log(table_data)
		// 	// console.log(formatted_html)
		// 	// frm.set_value("dashboard",formatted_html)
		// 	frm.set_df_property("dashboard","options",formatted_html)
		// 	frm.refresh_field("dashboard")
		// }
		// frm.set_query()
		frm.trigger("task_filter")




	},
	show_allocated_task(frm) {
		if (frm.doc.show_allocated_task) {
			frappe.call({
				doc: frm.doc,
				method: 'fetch_allocated_tasks',
				async: false,
				callback(r) {
					if (r.message) {
						// console.log(r.message)
						frm.set_value("task","")
						for (let i of r.message) {
							let row = frm.add_child("task")
							row.task = i.name
							row.subject = i.subject
							row.allocated_user = i.user
						}
						frm.refresh_field('task')
					}
				}
			})
		} else {
			frm.set_value("task", "")
		}
	},
	// send_update(frm){
	// 	console.log("send update triggered...")
	// 	frappe.confirm('Are you sure you want to proceed? It will send as update in your update group',
	// 		() => {
	// 			frappe.call({
	// 				doc:frm.doc,
	// 				method:"send_update",
	// 			})
	// 		}, () => {
	// 			// action to perform if No is selected
	// 		})
		
	// },

	task_filter(frm) {
		frm.fields_dict["task"].grid.get_field("task").get_query = function (doc) {
			return {
				filters: {
					project: frm.doc.project
				},
			};
		};
	},
	pending_tasks(frm) {
		// frm.set_value("pending_tasks",0)
			frappe.call({
				doc: frm.doc,
				method: "pending_task",
				async: false,
				callback(r) {
					if (r.message) {
						// console.log(r.message)
						let formatted_html = ''
						for (let i of r.message) {
							formatted_html += `<div style='border:1px solid #171717;border-radius:10px;margin-bottom:10px;display:flex;padding:10px;justify-content:space-around;align-items:center;'>
								<p style='margin:0;text-align:center;'>${i.project}</p>
								<p style='margin:0;text-align:center;'>${i.project_name}</p>
								<p style='margin:0;text-align:center;'>${i.count}</p>
							</div>`
						}
						let html = ""
						if(formatted_html){
							html +=`<div id='parent'>${formatted_html}</div>`
						}else{
							html+=`<div id='parent'>No Pending Tasks</div>`
						}
						// console.log(formatted_html)
						let d = new frappe.ui.Dialog({
							title: 'List of pending tasks',
							fields: [
								{
									"label": "",
									"fieldname": "task_table",
									"fieldtype": "HTML",
									"options": html
								}
							],
							size: "small",
							// primary_action_label: 'Submit',
							// primary_action(values) {
							// 	console.log(values);
							// 	d.hide();
							// }
						});
						d.show()

					}
				}
			})

	},
	project(frm) {
		frm.trigger("task_filter")

		if (frm.doc.project) {
			frappe.call({
				doc: frm.doc,
				method: "fetch_unallocated_tasks",
				args: {
					'project': frm.doc.project
				},
				async: false,
				callback(r) {
					if (r.message) {
						frm.set_value("task", "")
						for (let i of r.message) {
							let row = frm.add_child("task")
							row.task = i.name
							row.subject = i.subject
						}
					}
				}
			})
			frm.refresh_field("task")
		} else {
			frm.set_value("task", "")
		}
	},
});

frappe.ui.form.on("Task Allocation Item", {
	task(frm, cdt, cdn) {
		let d = locals[cdt][cdn]
		// console.log(d.task)
		if (d.task) {
			frappe.call({
				doc: frm.doc,
				method: "get_task_description",
				args: {
					"task": d.task
				},
				async: false,
				callback(r) {
					if (r.message) {
						d.subject = r.message
					}
				}
			})
			frm.refresh_field("task")
		}
	}
})
