// Copyright (c) 2018, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Screen Functionality', {
	refresh: function(frm) {
		console.log(frm)
			// frm.add_custom_button(__('Create Tasks'), function () {
			// 	frm.trigger("create_tasks");
			// });
	},
	// create_tasks: function (frm) {
	// 	frappe.call({
	// 		method: "go1_projects.go1_projects.doctype.screen_functionality.screen_functionality.create_tasks_for_checkpoints",
	// 		args: {},
	// 		callback: function (r) {
	// 			console.log(r.message);
	// 		},
	// 	})
	// }
});
