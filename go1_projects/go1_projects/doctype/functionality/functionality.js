// Copyright (c) 2018, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Functionality', {
  // after_save: function(frm) {
  //       var a;
  //       console.log(frm.doc.checkpoints)

  //       if (frm.doc.screen && frm.doc.module) {

  //           frappe.call({
  //             method: "frappe.client.get_value",
  //             args: {
  //               doctype: "Screen",
  //               filters: {"name": frm.doc.screen},
  //               fieldname: "development_task"
  //             },
  //             async: false,
  //             callback: function(r){
  //               a = r.message.development_task;
  //             }
  //           });


  //       }
  //       else if (frm.doc.module && !frm.doc.screen) {
           

  //           frappe.call({
  //             method: "frappe.client.get_value",
  //             args: {
  //               doctype: "Module",
  //               filters: {"name": frm.doc.screen},
  //               fieldname: "task"
  //             },
  //             async: false,
  //             callback: function(r){
  //               a = r.message.task;
  //             }
  //           });


  //       }

  //       frappe.call({
  //             method: "frappe.client.insert",
  //             args: {
  //                 doc: {
  //                     "doctype": "Task",
  //                     "subject": frm.doc.subject,
  //                     "status": frm.doc.status,
  //                     "project": frm.doc.project,
  //                     "parent_task": a,
  //                     "is_group": 1

  //                 }
  //             },
  //             callback: function(r) {
  //               console.log(r.message)
  //               frappe.call({
  //                 method: 'frappe.client.set_value',
  //                 args: {
  //                 doctype: "Functionality",
  //                 name: frm.doc.name,
  //                 fieldname: "task",
  //                 value: r.message.name,
  //               },
  //               freeze: true,
  //               callback: function(r) {
                  
  //               }
  //               });        

  //             }
  //         });


  // },



});























frappe.ui.form.on("Functionality", "onload", function(frm) {

  cur_frm.set_query("module", function() {
      return {
          "filters": {
              "project": frm.doc.project
          }
      };
  });

  cur_frm.set_query("screen", function() {
      return {
          "filters": {
              "project": frm.doc.project,
              "module": frm.doc.module
          }
      };
  });
  
});
