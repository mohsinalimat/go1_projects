// Copyright (c) 2017, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Module', {
	after_save: function(frm) {

if(frm.doc.task == null){
    frappe.call({
        method: "frappe.client.insert",
        args: {
            doc: {
                "doctype": "Task",
                "subject": frm.doc.module_name,
                "status": frm.doc.status,
                "project": frm.doc.project,
                "is_group": 1

            }
        },
        callback: function(r) {
          console.log(r.message)
          frappe.call({
            method: 'frappe.client.set_value',
            args: {
            doctype: "Module",
            name: frm.doc.name,
            fieldname: "task",
            value: r.message.name,
          },
          freeze: true,
          callback: function(r) {}
          });

        }
    });


}


    }
});



