function gi(listview) {
    // console.log(listview)
    var checked_bugs = [];
    var a2 = listview.get_checked_items();
    for (var i = 0; i < a2.length; i++) {
        checked_bugs.push(a2[i].name)
    }
    console.log(checked_bugs)
    if (checked_bugs.length > 0) {
        frappe.call({
            method: "go1_projects.go1_projects.doctype.functionality.functionality.get_users",
            args: {
                "names": checked_bugs,
            },
            callback: function(r) {
                console.log(r.message)
                if (r.message) {
                    var arr = [];
                    for (var i = 0; i < r.message.users.length; i++) {
                        if (r.message.users[i].name != "Administrator" && r.message.users[i].name != "Guest") {
                            arr.push({
                                "label": r.message.users[i][0],
                                "fieldname": r.message.users[i][0],
                                "fieldtype": "Check"
                            })
                        }
                    }
                    var d = new frappe.ui.Dialog({
                        title: __('Share'),
                        fields: arr,
                        primary_action: function() {
                            var obj = d.get_values();
                            var result = Object.keys(obj).map(function(key) {
                                return [(key), obj[key]];
                            });
                            // console.log(r.message.task)
                            var method = "go1_projects.go1_projects.doctype.functionality.functionality.post";
                            listview.call_for_selected_items(method, { "user": result, "task": r.message.task, "doctype": cur_list.doctype });
                            d.hide();
                        },
                        primary_action_label: __('Share')
                    });
                    d.show();
                } else { frappe.msgprint('Projects related to the Functionalities are not shared to any users!!!') }

            }
        });
    } else {
        frappe.msgprint("Please Select the Functionality to be shared")
    }
}

frappe.listview_settings['Functionality'] = {
    onload: function(listview) {
        listview.page.add_action_icon("fa fa-share-alt", function() {
            gi(listview)
        });

    }

};
