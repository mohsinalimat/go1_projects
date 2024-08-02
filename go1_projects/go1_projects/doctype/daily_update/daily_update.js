// Copyright (c) 2024, info@tridotstech.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Update', {
	setup(frm){
		// console.log("setup trigeered")
		frm.fields_dict["allocate_task"].grid.get_field("task").get_query = function (frm, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					project: child.project,
					status: ["!=", "Cancelled"],
				},
			};
		};
	},
	// onload(frm){
	// 	console.log("onload trigered")
	// },
	// onload_post_render: function (frm) {
		// var btn = $(this.wrapper).find(".grid-add-multiple-rows");

		// // show button

		// btn.removeClass("hidden");
		// // console.log(frm.get_field("items").grid)

		// // frm.get_field("allocate_task").grid.set_multiple_add("project");
		// // frm.get_field("allocate_task").grid.set_multiple_add("task",1)
		// $('[class="grid-add-multiple-rows btn btn-xs btn-secondary"]').on("click",function(){
		// 	set_multiple_adddd()
		// })
	// },

	add_multiple(frm) {
		let query_args = {
			query: "go1_projects.go1_projects.doctype.daily_update.daily_update.get_popup_query",
			filters: { status: ["!=", 'Completed'], exp_start_date: ['is', 'not set'] }
		}
		new frappe.ui.form.MultiSelectDialog({
			doctype: "Task",
			target: frm,
			setters: {
				// project:"",
			},
			size: "large",
			add_filters_group: 1,
			get_query() {
				return {
					query: "go1_projects.go1_projects.doctype.daily_update.daily_update.get_popup_query",
					filters: { status: ["!=", 'Completed'], exp_start_date: ['is', 'not set'] }
				}
			},
			columns: ["name", "subject", "description"],
			action(selections) {
				// console.log(selections);
				// frappe.call({

				// })
				for (let i of selections) {
					frm.call({
						doc: frm.doc,
						method: "get_task_details",
						args: {
							task: i
						},
						async: false,
						callback(r) {
							let task = r.message
							let child = frm.add_child("allocate_task")
							child.task = i
							child.subject = task.subject
							child.description = task.description
							child.project = task.project
						}
					})
				}
				frm.refresh_field("allocate_task")
			}
		});



		// setTimeout(function(){
		// $('[data-fieldname="results_area"]').change(function(){
		// 	// alert("working...")
		// 	console.log("test working...")
		// })
		// Check every 100 milliseconds
		// $('[class="modal-dialog modal-xl"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').find('[class="list-item__content ellipsis"]:last .ellipsis').attr("style","white-space: normal !important;")

		// $('[class="modal-dialog modal-xl"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').find('[class="list-item__content ellipsis"]:last').attr("style","height: 42px !important;align-items: start !important;overflow: auto !important;")

		// $('[class="modal-dialog modal-xl"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').attr("style","height:50px;")

		// $('[class="btn btn-secondary btn-xs clear-filters"]').on('click',function(){
		// 	setTimeout(function(){
		// 		$('[class="modal-dialog modal-xl"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').find('[class="list-item__content ellipsis"]:last .ellipsis').attr("style","white-space: normal !important;")

		// 		$('[class="modal-dialog modal-xl"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').find('[class="list-item__content ellipsis"]:last').attr("style","height: 42px !important;align-items: start !important;overflow: auto !important;")

		// 		$('[class="modal-dialog modal-xl"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').attr("style","height:50px;")


		// 	},100)
		// })

		// },500)
		var counter = 0
		var checkExist = setInterval(function () {
			var $resultsArea = $('[data-fieldname="results_area"]');
			// console.log(counter++);
			// console.log($resultsArea.children().length)
			if ($resultsArea.children().length > 0) {
				// Apply CSS to elements within the modal-content container
				$('[class="modal-dialog modal-lg"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').find('[class="list-item__content ellipsis"]:last .ellipsis').attr("style", "white-space: normal !important;");

				$('[class="modal-dialog modal-lg"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').find('[class="list-item__content ellipsis"]:last').attr("style", "height: 42px !important;align-items: start !important;overflow: auto !important;");

				$('[class="modal-dialog modal-lg"] [data-fieldname="results_area"] [class="list-item-container"] [class="list-item"]').attr("style", "height:55px;");

				// clearInterval(checkExist);
			}
		}, 100);


	},
	refresh: function (frm) {
		// frm.set_query('task','allocate_tasks',function(frm,cdt,cdn){
		// 	let row = locals[cdt][cdn]
		// 	return {
		// 		"filters":{
		// 			"project":row.project
		// 		}
		// 	}
		// });
		$('.indicator-pill').hide()
		$('[class="grid-add-multiple-rows btn btn-xs btn-secondary hidden"]').removeClass("hidden");
		$('[class="grid-add-multiple-rows btn btn-xs btn-secondary"]').on("click", function () {
			frm.trigger("add_multiple")

		})
		frm.disable_save()
		// frm.add_custom_button('Test', function () {
		// 	frappe.call({
		// 		method: "go1_projects.api.mail_reports_to",
		// 		async: false,
		// 		callback(r) {

		// 		}
		// 	})
		// })

		frm.add_custom_button('Send Update', function () {
			if (frm.doc.allocate_task.length > 0) {
				frappe.confirm('Are you sure you want to proceed? It will send as update in your update group',
					() => {
						frappe.call({
							doc: frm.doc,
							method: "send_update",
							async: false,
							callback: function (r) {
								// frm.set_value("allocate_task", "")
								if (r.message) {
									if (r.message == "Create Log Success") {
										frappe.msgprint("Morning update scheduled successfully")
										setTimeout(function () {
											frm.reload_doc()
										}, 2000)
									}
									if (r.message == "assigned") {
										frappe.msgprint("Timesheet and update scheduled successfully")
									}
								}
							}
						})
					}, () => {
						// action to perform if No is selected
					})
			} else {
				frappe.throw("There are no tasks to send update")
			}
		})
		frm.set_value("start_date", frappe.datetime.now_date())
		frm.trigger("get_my_tasks")

	},
	get_my_tasks(frm) {
		frappe.call({
			doc: frm.doc,
			method: "fetch_pending_tasks",
			async: false,
			callback: function (r) {
				if (r.message) {
					// console.log("calling tasks")
					// console.log(r.message)
					frm.set_value("allocate_task", "")
					for (let i of r.message) {
						let row = frm.add_child("allocate_task")
						row.task = i.name
						row.subject = i.subject
						row.project = i.project
						row.description = i.description
						row.expected_hours = i.expected_time
					}
					// frm.refresh()
					$('[data-label="%20Save"]').hide()
					$('[data-label="Start%20Timer"]').hide()
					$('[data-label="Resume%20Timer"]').hide()
				} else {
					frm.trigger("get_my_works")
				}
			}
		})
	},
	start_date(frm) {
		frm.trigger("get_my_tasks")
	},
	update_log(frm) {
		frm.call({
			doc: frm.doc,
			method: "update_my_log",
			async: false,
			callback: function (r) {
				frappe.show_alert('Daily update has updated', 5);
			}
		})
	},
	get_my_works(frm) {
		frm.call({
			doc: frm.doc,
			method: "get_my_works",
			async: false,
			callback(r) {
				// console.log(r.message)
				if (r.message) {
					frm.add_custom_button(" Save", function () {
						frm.call({
							doc: frm.doc,
							method: "update_my_log",
							// async: false,
							callback: function (r) {
								frappe.show_alert('Daily update has updated', 5);
								frm.reload_doc()
							}
						})
					})
					frm.set_value("allocate_task", "")
					for (let i of r.message) {
						let row = frm.add_child("allocate_task")
						row.project = i.project
						row.project_name = i.project_name
						row.subject = i.subject
						row.task = i.task
						row.description = i.description
						row.expected_hours = i.expected_hrs
						row.actual_hours = i.actual_hrs
						row.status = i.status
						row.from_time_update = i.from_time
						row.to_time = i.to_time
						row.started = i.started
						row.completed = i.completed
						row.activity = i.activity
					}
					// let df = frappe.meta.get_docfield("Self Allocation","expected_hours",cur_frm.doc.name)
					// df.read_only=1
					frm.trigger("timer_func")
					frm.refresh_field("allocate_task")
					frm.change_custom_button_type(__(" Save"), null, "primary");
					$('[data-label="%20Save"]').show()
					$('[data-label="Start%20Timer"]').show()
					$('[data-label="Resume%20Timer"]').show()
				} else {
					frm.set_value("allocate_task", "")
					frm.refresh()
					// frm.disable_save()
				}
			}
		})
	},
	timer_func(frm) {
		let button = "Start Timer";
		$.each(frm.doc.allocate_task || [], function (i, row) {
			if (row.from_time_update <= frappe.datetime.now_datetime && row.started && !row.completed) {
				button = "Resume Timer";
			}
		});
		frm.add_custom_button(__(button), function () {
			var flag = true;
			// go1_projects.daily_update.timer(frm)
			if (button == "Start Timer") {
				go1_projects.daily_update.timer(frm)
			}
			$.each(frm.doc.allocate_task || [], function (i, row) {
				// Fetch the row for which from_time is not present
				// if (flag && row.activity_type && !row.from_time) { core functionality
				// if (!row.from_time) {
				// 	go1_projects.daily_update.timer(frm, row);
				// 	row.from_time = frappe.datetime.now_datetime();
				// 	frm.refresh_fields("allocate_task");
				// 	frm.save();
				// 	flag = false;
				// }
				// // Fetch the row for timer where activity is not completed and from_time is before now_time
				if (row.started && row.from_time_update <= frappe.datetime.now_datetime() && !row.completed && !row.to_time) {
					let timestamp = moment(frappe.datetime.now_datetime()).diff(
						moment(row.from_time_update),
						"seconds"
					);
					// console.log("calling from resume timer",timestamp)
					go1_projects.daily_update.timer(frm, row, timestamp);
				}
			})
			// 	flag = false;
			// }
			// });
			// If no activities found to start a timer, create new
			// if (flag) {
			// 	erpnext.timesheet.timer(frm);
			// }
		}).addClass("btn-primary");
	}
});


frappe.ui.form.on("Daily Update Item", {
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
						let row = frm.selected_doc;
						if (row.task) {
							frappe.db.get_value("Task", row.task, "project", (r) => {
								frappe.model.set_value(cdt, cdn, "project", r.project);
							});
						}
					// console.log(r.message);
					if (r.message) {
						d.subject = r.message[0]
						d.description = r.message[1]
						d.project = r.message[2]
						d.expected_hours = r.message[3]
						frm.refresh_field("allocate_task")
					}
				}
			})
		}
	},
	from_time_update(frm, cdt, cdn) {
		// calculate_end_time(frm, cdt, cdn);
		var d = locals[cdt][cdn]
		if (d.to_time) {
			const parsedTimestamp1 = new Date(d.from_time_update);
			const parsedTimestamp2 = new Date(d.to_time);

			// Calculate the difference in milliseconds
			const differenceInMilliseconds = parsedTimestamp2 - parsedTimestamp1;

			// Convert the difference from milliseconds to hours
			const differenceInHours = differenceInMilliseconds / (1000 * 60 * 60);

			// console.log(differenceInHours)
			d.actual_hours = differenceInHours
			frm.refresh_field("allocate_task")
		}
	},
	to_time(frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		if (d.from_time_update) {
			const parsedTimestamp1 = new Date(d.from_time_update);
			const parsedTimestamp2 = new Date(d.to_time);

			// Calculate the difference in milliseconds
			const differenceInMilliseconds = parsedTimestamp2 - parsedTimestamp1;

			// Convert the difference from milliseconds to hours
			const differenceInHours = differenceInMilliseconds / (1000 * 60 * 60);

			// console.log(differenceInHours)
			d.actual_hours = differenceInHours
			frm.refresh_field("allocate_task")
		}
	}

});
