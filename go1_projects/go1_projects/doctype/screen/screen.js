// Copyright (c) 2017, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Screen', {

	after_save: function(frm) {
		var a;


	frappe.call({
		method: 'frappe.client.get_value',
		args:{
			'doctype': 'Module',
			filters: {"name": frm.doc.module},
			fieldname: "task"
		},
		async: false,
		callback: function (r) {
			// body...
			a = r.message;
		}

	});
	console.log(a)
if(frm.doc.task == null){
    frappe.call({
        method: "frappe.client.insert",
        args: {
            doc: {
                "doctype": "Task",
                "subject": frm.doc.screen_name,
                "status": frm.doc.status,
                "project": frm.doc.project,
                "parent_task": a.task,
                "is_group": 1

            }
        },
        callback: function(r) {
          console.log(r.message)
          frappe.call({
            method: 'frappe.client.set_value',
            args: {
            doctype: "Screen",
            name: frm.doc.name,
            fieldname: "task",
            value: r.message.name,
          },
          freeze: true,
          callback: function(r) {}
          });
              frappe.call({
                  method: "frappe.client.insert",
                  args: {
                      doc: {
                          "doctype": "Task",
                          "subject": frm.doc.screen_name+"(Developement)",
                          "status": frm.doc.status,
                          "project": frm.doc.project,
                          "parent_task": r.message.name,
                          "is_group": 1

                      }
                  },
                  async: false,
                  callback: function(r) {
                    console.log(r.message)
                    frappe.call({
                      method: 'frappe.client.set_value',
                      args: {
                      doctype: "Screen",
                      name: frm.doc.name,
                      fieldname: "development_task",
                      value: r.message.name,
                    },
                    freeze: true,
                    callback: function(r) {}
                    });
                  }
              });
              frappe.call({
                  method: "frappe.client.insert",
                  args: {
                      doc: {
                          "doctype": "Task",
                          "subject": frm.doc.screen_name+"(Testing)",
                          "status": frm.doc.status,
                          "project": frm.doc.project,
                          "parent_task": r.message.name,
                          "is_group": 1

                      }
                  },
                  callback: function(r) {
                    console.log(r.message)
                    // frm.set_value("testing_task", r.message.name);
                    frappe.call({
                      method: 'frappe.client.set_value',
                      args: {
                      doctype: "Screen",
                      name: frm.doc.name,
                      fieldname: "testing_task",
                      value: r.message.name,
                    },
                    freeze: true,
                    callback: function(r) {}
                    })

                  }
              });
        

        }
    });


}


	}
});
frappe.ui.form.on("Screen", "onload", function(frm) {

  cur_frm.set_query("module", function() {
      return {
          "filters": {
              "project": frm.doc.project
          }
      };
  });

  
});
