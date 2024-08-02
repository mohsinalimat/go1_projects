function gi(listview) {
            // console.log(listview)
            var checked_bugs = [];
            var a2 = listview.get_checked_items();
            for (var i=0; i<a2.length; i++){
                checked_bugs.push(a2[i].name)
            }
            // debugger;
            if (checked_bugs.length > 0) {
                frappe.call({
                    method: "go1_projects.go1_projects.doctype.bug_sheet.bug_sheet.get_users",
                    args: {
                        "names": checked_bugs,
                    },
                    callback: function(r) {
                        console.log(r.message)
                       if(r.message){
                            var arr = [];
                            for (var i = 0; i < r.message.length; i++) {
                                if (r.message[i].name != "Administrator" && r.message[i].name != "Guest") {
                                    arr.push({
                                        "label": r.message[i][0],
                                        "fieldname": r.message[i][0],
                                        "fieldtype": "Check"
                                    })
                                }
                            }
                            var d = new frappe.ui.Dialog({
                                title: __('Share Bugs'),
                                fields: arr,
                                primary_action: function() {
                                    var obj = d.get_values();
                                    var result = Object.keys(obj).map(function(key) {
                                        return [(key), obj[key]];
                                    });
                                    console.log(result)
                                    var method = "go1_projects.go1_projects.doctype.bug_sheet.bug_sheet.post";
                                    listview.call_for_selected_items(method, { "user": result, "doctype": cur_list.doctype });
                                    d.hide();
                                },
                                primary_action_label: __('Share Bugs')
                            });
                            d.show();
                        }
                        else{frappe.msgprint('Projects related to the bugs are not shared to any users!!!')}

                    }
                });
            } else {
                frappe.msgprint("Please Select the Bugs to be shared")
            }
}


function vi(listview) {
        var zTreeObj;
        function myOnClick(event, treeId, treeNode) {
            
                    $('[data-fieldname="project"]').val(null);
                    $('[data-fieldname="module"]').val(null);
                    $('[data-fieldname="screen"]').val(null);
                if(treeNode.type == 'project')
                    {
                         
                         frappe.set_route("List", cur_list.doctype, {
                                'project': treeNode.idname,
                                'module': null,
                                'screen': null
                         });   

                    }
                if(treeNode.type == 'module')
                    {    
                         
                         frappe.set_route("List", cur_list.doctype, {
                                'project': treeNode.getParentNode().idname,
                                'module': treeNode.idname,
                                'screen': null
                         });                          

                    }
                if(treeNode.type == 'screen')
                    {
                         
                         frappe.set_route("List", cur_list.doctype, {
                                'project': treeNode.getParentNode().getParentNode().idname,
                                'module': treeNode.getParentNode().idname,
                                'screen': treeNode.idname,
                         });                              

                    }
                else{
                    return null;
                }
        };
        var setting = {
            callback: {
                onClick: myOnClick
            }
        };
        var a;

        frappe.call({
            method: 'go1_projects.go1_projects.doctype.bug_sheet.bug_sheet.get_tree_data',
            async: false,
            callback: function (r) {
                a = r.message;
            }
        })  

        function go(a) {
            var arr = [];

                for (var i=0; i<a.projects.length; i++) {
                  arr.push({'name': a.projects[i].Project_name, 'open': a.projects[i].open,
                            'children': construct_modules(a.projects[i].name, a),
                            'type': 'project', 'idname': a.projects[i].name
                            })
                }

            return arr    
        }

        function construct_modules(u,a){
            var arr1 = [];
            for (var i = 0; i < a.modules.length; i++) {
                if (a.modules[i].project == u) {
                    arr1.push({'name': a.modules[i].module_name, 'open': a.modules[i].open,
                            'children': construct_screens(a.modules[i].name, a),
                            'type': 'module', 'idname': a.modules[i].name
                            })
                }
            }
            return arr1
        }

        function construct_screens(u,a) {
            var arr2 = [];
            for (var i = 0; i < a.screens.length; i++) {
                if (a.screens[i].module == u) {
                    arr2.push({'name': a.screens[i].screen_name, 'open': a.screens[i].open,
                            'type': 'screen', 'idname': a.screens[i].name
                            })
                }
            }
            return arr2
        }

        function construct_bugs(u,a) {
            var arr3 = [];
            for (var i = 0; i < a.bugs.length; i++) {
                if (a.bugs[i].screen == u) {
                    arr3.push({'name': a.bugs[i].bug_title,
                             'type': 'bug', 'idname': a.bugs[i].name
                             })
                }
            }
            return arr3
        }


        var zNodes = go(a)

        // $(document).ready(function() {
            
        //     $(".filter_list").html('<ul id="treeDemo" class="ztree"></ul>');
        //     zTreeObj = $.fn.zTree.init($("#treeDemo"), setting, zNodes);
        // });

}
frappe.listview_settings['Bug Sheet'] = {
    add_fields: ["status", "priority"],
    onload: function(listview) {
        // listview.page.fields_dict.module.get_query = function(doc) {
        //     return { filters: { project: listview.page.fields_dict.project.value } }
        // }
        // listview.page.fields_dict.screen.get_query = function(doc) {
        //     return { filters: { project: listview.page.fields_dict.project.value, module: listview.page.fields_dict.module.value } }
        // }

        listview.page.add_action_icon("fa fa-share-alt", function() {
            gi(listview)
        });
    	// vi(listview);

    },
    refresh: function (listview) {
        // vi(listview);
    },
    before_render: function(listview) {
        // vi(listview);
    },
    get_indicator: function(doc) {
        
        if (doc.status == "Fixed") {
            return [__("Fixed"), "orange"];
        } else if (doc.status == "Verified") {
            return [__("Verified"), "green"];
        } else if (doc.status == "Open") {
            return [__("Open"), "red"];
        } else if (doc.status == "Re-open") {
            return [__("Re-open"), "red"];
        } else if (doc.status == "Closed") {
            return [__("Closed"), "blue"];
        }
        if (doc.priority == "High") {
            return [__("High"), "red"];
        } else if (doc.priority == "Medium") {
            return [__("Medium"), "black"];
        } else if (doc.priority == "Low") {
            return [__("Low"), "green"];
        }

    }

};