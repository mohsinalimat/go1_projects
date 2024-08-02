// Copyright (c) 2017, Valiant Systems  and contributors
// For license information, please see license.txt
// function yu() {
//     var a;

//     frappe.call({
//         method: 'pms.pms.doctype.bug_sheet.bug_sheet.get_tree_data',
//         async: false,
//         callback: function(r) {
//             a = r.message;
//         }
//     })

//     function go_go(a) {
//         var arr = [];

//         var l = a.projects.length + 1;
//         var m = a.modules.length + a.projects.length;
//         for (var i = 0; i < a.projects.length; i++) {
//             var ab = i + 1;
//             arr.push({ id: ab, pId: 0, name: a.projects[i].Project_name, open: a.projects[i].open, type: a.projects[i].type, docname: a.projects[i].name })


//             for (var j = 0; j < a.modules.length; j++) {

//                 if (a.modules[j].project == a.projects[i].name) {

//                     arr.push({ id: l, pId: ab, name: a.modules[j].module_name, open: a.modules[j].open, type: a.modules[j].type, docname: a.modules[j].name })

//                     for (var k = 0; k < a.screens.length; k++) {

//                         if (a.screens[k].module == a.modules[j].name) {
//                             arr.push({ id: m, pId: l, name: a.screens[k].screen_name, open: a.screens[k].open, type: a.screens[k].type, docname: a.screens[k].name })
//                             m = m + 1;
//                         }

//                     }
//                     l = l + 1;

//                 }

//             }

//         }

//         return arr
//     }

//     var setting = {
//         view: {
//             dblClickExpand: false
//         },
//         data: {
//             simpleData: {
//                 enable: true
//             }
//         },
//         callback: {
//             beforeClick: beforeClick,
//             onClick: onClick
//         }
//     };
//     var zNodes = go_go(a);


//     function beforeClick(treeId, treeNode) {
//         // var check = (treeNode && !treeNode.isParent);
//         // if (!check) alert("Do not select province...");
//         // return check;
//     }

//     function onClick(e, treeId, treeNode) {

//         var zTree = $.fn.zTree.getZTreeObj("treeDemo"),
//             nodes = zTree.getSelectedNodes(),
//             v = "";
//         console.log(nodes)


//         if (nodes.length > 1) {
//             var pro = [];
//             var mod = [];
//             var scr = [];
//             for (var j = 0; j < nodes.length; j++) {
//                 if (nodes[i].type == 'projects') {
//                     pro.push(treeNode.docname)
//                 }
//                 if (nodes[i].type == 'modules') {
//                     mod.push(treeNode.docname)
//                 }
//                 if (nodes[i].type == 'screens') {
//                     scr.push(treeNode.docname)
//                 }
//             }
//             console.log(pro)
//         } else if (nodes.length <= 1) {
//             var tu = '';
//             if (treeNode.type == 'projects') {
//                 tu = { "project": treeNode.docname }
//             }
//             if (treeNode.type == 'modules') {
//                 tu = {
//                     "project": treeNode.getParentNode().docname,
//                     "module": treeNode.docname
//                 }
//             }
//             if (treeNode.type == 'screens') {
//                 tu = {
//                     "project": treeNode.getParentNode().getParentNode().docname,
//                     "module": treeNode.getParentNode().docname,
//                     "screen": treeNode.docname
//                 }
//             }
//         }


//         nodes.sort(function compare(a, b) { return a.id - b.id; });
//         for (var i = 0, l = nodes.length; i < l; i++) {
//             v += nodes[i].name + ",";
//         }
//         if (v.length > 0) v = v.substring(0, v.length - 1);
//         var cityObj = $("#citySel");
//         if (treeNode.type == 'projects') {
//             v = 'Project: ' + v
//         }
//         if (treeNode.type == 'modules') {
//             v = 'Module: ' + v
//         }
//         if (treeNode.type == 'screens') {
//             v = 'Screen: ' + v
//         }
//         cityObj.attr("value", v);



//         frappe.call({
//             method: 'frappe.client.get_list',
//             args: {
//                 doctype: 'Bug Sheet',
//                 fields: ['name', 'bug_title'],
//                 filters: tu
//             },
//             callback: function(r) {
//                 console.log(r.message)
//                 var pop = '';
//                 if (r.message) {
//                     for (var i = 0; i < r.message.length; i++) {

//                         $('#menuContent').hide();
//                         $('#listContent').show();
//                         pop = pop + '<div href="#Form/Bug%20Sheet/' + r.message[i].name + '" \
//                                         data-link="Form/Bug%20Sheet/' + r.message[i].name + '" \
//                                         onclick="detailfield(this)" \
//                                         style="padding:12px; border-bottom: 1px solid #e6e2e2;" \
//                                         class="sel">\
//                                         <h2 style="font-size: 12px; font-weight: 500; margin: 0;  color: #333;">\
//                                         <strong>' + r.message[i].bug_title + '</strong>\
//                                         </h2> </div>'

//                     }
//                 }
//                 $('#listContent').html(pop);
//             }
//         })
//     }

//     function showMenutree() {
//         var cityObj = $("#citySel");
//         var cityOffset = $("#citySel").offset();
//         $("#menuContent").css({ left: 0 + "px", top: 25 + "px" }).slideDown("fast");

//         $("body").bind("mousedown", onBodyDown);
//     }

//     function hideMenu() {
//         $("#menuContent").fadeOut("fast");
//         $("body").unbind("mousedown", onBodyDown);
//     }

//     function onBodyDown(event) {
//         if (!(event.target.id == "menuBtn" || event.target.id == "menuContent" || $(event.target).parents("#menuContent").length > 0)) {
//             hideMenu();
//         }
//     }

//     $('.filter_list').html('<input id="citySel" type="text" placeholder="Filters" readonly value="" style="width: 100%;margin-left: 0;border: 1px solid transparent;padding: 5px 10px;margin-top: 0px;border-right: 1px solid rgb(221, 221, 221);border-bottom: 1px solid rgb(221, 221, 221);border-left: 1px solid rgb(221, 221, 221);"/>');
//     $('.filter_list').append('<div id="menuContent" class="menuContent" style="display:none; position: absolute;"> <ul id="treeDemo" class="ztree" style="margin-top:0; width:100%;"></ul> </div>');
//     $('.filter_list').append('<div id="listContent" style="display:block; position: absolute; width: 100%;"></div>');
//     $.fn.zTree.init($("#treeDemo"), setting, zNodes);
//     $('#citySel').click(function() {
//         $('#listContent').hide();
//         showMenutree();
//     });


// }
frappe.ui.form.on('Bug Sheet', {
    onload: function(frm) {
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
        // yu()
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Bug Sheet',
                fields: ['name', 'bug_title']
            },
            callback: function(r) {
                var pop = '';
                if (r.message) {
                    for (var i = 0; i < r.message.length; i++) {

                        $('#menuContent').hide();
                        $('#listContent').show();
                        pop = pop + '<div href="#Form/Bug%20Sheet/' + r.message[i].name + '" \
                                        data-link="Form/Bug%20Sheet/' + r.message[i].name + '" \
                                        onclick="detailfield(this)" \
                                        style="padding:12px; border-bottom: 1px solid #e6e2e2;" \
                                        class="sel">\
                                        <h2 style="font-size: 12px; font-weight: 500; margin: 0;  color: #333;">\
                                        <strong>' + r.message[i].bug_title + '</strong>\
                                        </h2> </div>'

                    }
                }
                $('#listContent').html(pop);
            }
        })
    },
    refresh: function(frm) {
        // yu()
        if (frm.doc.issue_type){
            load_screening_fileds(frm,flag=0)
            let value = JSON.parse(frm.doc.issue_screening_json);
            for(let i of value){
                if (i.field_type == "Checkboxes"){
                    $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}"]`).prop("checked",i.value)
                }
                else if(i.field_type == "User Picker (Multiple Users)" || i.field_type == "Group Picker (multiple groups)"){
                    $(`[data-fieldname="${i.field_name}"]`).find('.table-multiselect').prepend(i.value)
                }
                else if(i.field_type == "Select list (Cascading)"){
                    
                    $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}`).prop("value",i.value1)
                    for(let opt of i.options){
                        $(`select[data-fieldname="${i.field_name}_cascade"]`).append(`<option value="${opt}">${opt}</option>`)
                    }
                    $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}_cascade"]`).prop("value",i.value2)
                }
                else{
                    $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}`).prop("value",i.value)
                }
            }
            frm.call({
                doc:frm.doc,
                method: 'get_workflow_action',
                async:false,
                callback:function(r){
                    for(let i of r.message){
                        frm.add_custom_button(`${i.action}`,()=>{
                            frappe.confirm('Are you sure you want to proceed?',
                                () => {
                                    frm.set_value("status",i.next_state)
                                    frm.save()
                                }, () => {
                
                                }
                            )
            
                        },"Actions")
                        
                    }
                    $('.inner-group-button button').removeClass("btn-default").addClass("btn-primary")
                    
                }
                
            })
                
            
            
        }
       
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Bug Sheet',
                fields: ['name', 'bug_title']
            },
            callback: function(r) {
                var pop = '';
                if (r.message) {
                    for (var i = 0; i < r.message.length; i++) {

                        $('#menuContent').hide();
                        $('#listContent').show();
                        pop = pop + '<div href="#Form/Bug%20Sheet/' + r.message[i].name + '" \
                                        data-link="Form/Bug%20Sheet/' + r.message[i].name + '" \
                                        onclick="detailfield(this)" \
                                        style="padding:12px; border-bottom: 1px solid #e6e2e2;" \
                                        class="sel">\
                                        <h2 style="font-size: 12px; font-weight: 500; margin: 0;  color: #333;">\
                                        <strong>' + r.message[i].bug_title + '</strong>\
                                        </h2> </div>'

                    }
                }
                $('#listContent').html(pop);
            }
        })
        if (frm.doc.project){
                frm.set_query("issue_type", function() {
                   return {
                        "query":"pms.pms.doctype.bug_sheet.bug_sheet.get_allowed_issue_types",
                        "filters": {
                             "project":frm.doc.project
                        }
                    }; 
                })
                
            }
        
    },
     project:function(frm){
             if (frm.doc.project){
                frm.set_query("issue_type", function() {
                   return {
                        "query":"pms.pms.doctype.bug_sheet.bug_sheet.get_allowed_issue_types",
                        "filters": {
                             "project":frm.doc.project
                        }
                    }; 
                })
                
            }
    },
    // validate: function(frm){
    //     frm.call({
    //         doc:frm.doc,
    //         method:"get_issue_type_screening",
    //         async:false,
    //         callback : function(r){
    //             res = r.message
                
    //         }
    //     })
    // },
    before_save: function(frm){
        
        frm.call({
            doc:frm.doc,
            method:"get_issue_type_screening",
            async:false,
            callback : function(r){
                res = r.message
                
                frm.set_value("issue_screening_json","")
                frm.refresh_field("issue_screening_json")
                let json_= []

               async function set_json(){ 
                    for(let i of res.message){
                        if (i.field_type == "Checkboxes"){
                            value = $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}"]`).prop("checked")
                            json_.push({    "field_name":i.field_name,
                                            "field_type":i.field_type,
                                            "reqd":i.reqd,
                                            "value":value
                                        })
                        }
                        else if(i.field_type == "User Picker (Multiple Users)" || i.field_type == "Group Picker (multiple groups)"){
                            let multi = ''
                            for(let j of $(`[data-fieldname="${i.field_name}"]`).find('.table-multiselect :button')){
                                multi += j.outerHTML
                            }
                            json_.push({
                                "field_name":i.field_name,
                                "field_type":i.field_type,
                                "reqd":i.reqd,
                                "value": multi
                            })
                        }
                        
                        
                        else if(i.field_type == "Select list (Cascading)"){
                            value1 = $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}"]`).val()
                            value2 = $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}_cascade"]`).val()
                            await frappe.db.get_doc("Issue Custom Fields",i.field_label).then( (r)=> {
                                if(r.cascading_options.length != 0){
                                    for(let row of r.cascading_options){
                                        if(row.parent_option == value1){
                                            frm.options = row.options.split('\n')
                                        }
                                    }
                                }
                                json_.push({    "field_name":i.field_name,
                                                "field_type":i.field_type,
                                                "reqd":i.reqd,
                                                "value1":value1,
                                                "value2":value2,
                                                "options":frm.options ? frm.options : ""
                                            })
                                
                            })
                            
                            
                            
                        }
                        else{
                            value = $(`[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}"]`).val()
                            json_.push({    "field_name":i.field_name,
                                            "field_type":i.field_type,
                                            "reqd":i.reqd,
                                            "value":value
                                        })
                            
                        }
                    }
                    frm.set_value("issue_screening_json",JSON.stringify(json_))
                    frm.refresh_field("issue_screening_json")
                    console.log("JSONNN = ",JSON.parse(frm.doc.issue_screening_json))
                    for(let j of JSON.parse(frm.doc.issue_screening_json)){
                        if(j.field_type == "URL Field"){
                            if(j.value != ""){
                                var valid = /^(ftp|http|https):\/\/[^ "]+$/.test(j.value);
                                if (valid == false){
                                    frm.dirty()
                                    frappe.validated=false
                                    frappe.throw("Enter Valid URL")
                                }
                            }
                            
                        }
                        if (j.reqd == 1 && (j.value == "" || j.value == null)  && j.field_type != "Checkboxes"){
                            frm.dirty()
                            frappe.validated=false
                            console.log("j.value = ",j.value)
                            frappe.throw("Mandatory fields are required")
                        }
                    }
                }
                set_json()
                
            }
        })
    },

    issue_type: function(frm){
        if (frm.doc.issue_type){
            frm.set_value("issue_screening_json","")
            frm.refresh_field("issue_screening_json")
            load_screening_fileds(frm,flag = 1)
        }
        frm.call({
            doc:frm.doc,
            method:"get_first_state",
            async:false,
            callback : function(r){
                    frm.set_value("status",r.message)
                    frm.refresh_field("status")
                    cur_frm.clear_custom_buttons()
            }
        })
    }
});

function load_screening_fileds(frm,flag = 0) {
    let type = {
        "Text Field (Single Line)":"Data",
        "Text Field (Multi-Line)":"Small Text",
        "Select list (Single choice)":"Select",
        "Date Picker":"Date",
        "Number field":"Int",
        "URL Field":"Data",
        "User Picker (Single User)":"Link",
        "User Picker (Multiple Users)":"Table MultiSelect",
        "Checkboxes":"Check",
        "Text Field (read only)":"Data",
        "Labels":"Data",
        "Date Time Picker":"Datetime",
        "Select list (Cascading)":"Select",
        "Group Picker (single group)":"Link",
        "Group Picker (multiple groups)":"Table MultiSelect",
        "Radio Buttons":"Select",
        "String - Story Points PL":"Data"
    }
    frm.call({
        doc:frm.doc,
        method:"get_issue_type_screening",
        args:{
            flag:flag
        },
        async:false,
        callback : function(r){
            res = r.message
            if(res.status == "Success"){

                $('[data-fieldname="section_break_ebad"] div[class="section-head"]').remove()
                $('[data-fieldname="section_break_ebad"]').prepend(`<div class="section-head">${frm.doc.issue_type}</div>`)
                $('[data-fieldname="issue_screen_html"]').attr("style","display: flex;width: 100%;flex-wrap: wrap;")
                $('[data-fieldname="__column_4"]').attr("style","padding:0px !important")
                cur_frm.fields_dict.issue_screen_html.$wrapper.empty()
                for(let i of res.message){
                    if (i.field_type == "Text Field (Single Line)" || i.field_type == "Number field" || i.field_type == "Date Picker" || i.field_type == "Checkboxes" || i.field_type == "Date Time Picker" || i.field_type == "String - Story Points PL"){
                        frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": `${type[i.field_type]}`,
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "reqd": i.reqd
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                        
                        
                    }
                    if (i.field_type == "Text Field (Multi-Line)"){
                        frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": `${type[i.field_type]}`,
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "reqd": i.reqd
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-12')
                        
                        
                    }
                    if (i.field_type == "URL Field"){
                        frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": `${type[i.field_type]}`,
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "reqd": i.reqd,
                                "options":"URL"
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                        
                        
                    }
                    if (i.field_type == "Select list (Cascading)"){
                        let input =  frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": `${type[i.field_type]}`,
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "options":`${i.options}`,
                                "reqd": i.reqd,
                                "onchange": function(){
                                    frm.value = this.get_value()
                                    $(`select[data-fieldname="${i.field_name}_cascade"]`).empty()
                                    frappe.db.get_doc("Issue Custom Fields",i.field_label).then( (r)=> {
                                        if(r.cascading_options.length != 0){
                                            for(let row of r.cascading_options){
                                                if(row.parent_option == frm.value){
                                                    frm.options = row.options.split('\n')
                                                    
                                                    // $(`select[data-fieldname="${i.field_name}_cascading"]`).append(`<option value="${opt}">Status</option>`)
                                                }
                                            }
                                            for(let opt of frm.options){
                                                $(`select[data-fieldname="${i.field_name}_cascade"]`).append(`<option value="${opt}">${opt}</option>`)
                                            }
                                        }
                                    })
                                    // frappe.ui.form.make_control({
                                    //     parent: this.$wrapper,
                                    //     df: {
                                    //         "fieldtype": `${this.df.fieldtype}`,
                                    //         "options":`IJK`
                                    //     },
                                    //     render_input:true
                                    // })
                                }
                            },
                            render_input:true
                        })
                        
                        
                        frm.html = ""
                        frm.html += `<div class="control-input-wrapper">
                                        <div class="control-input flex align-center">
                                            <select type="text" autocomplete="off" class="input-with-feedback form-control ellipsis" maxlength="140" data-fieldtype="Select" data-fieldname="${i.field_name}_cascade" placeholder="">
                                            </select>
                                            <div class="select-icon ">
                                                <svg class="icon  icon-sm" style="" aria-hidden="true">
                                                    <use class="" href="#icon-select"></use>
                                                </svg>
                                            </div>
                                        </div>
                                        <div class="control-value like-disabled-input" style="display: none;"></div>
                                        <p class="help-box small text-muted"></p>
                                    </div>`
                        $(`div[data-fieldname="${i.field_name}"] [class="form-group"]`).append(frm.html)
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                        
                    }
                    if (i.field_type == "Select list (Cascading)"){
                        frm.value = $(`div[data-fieldname="${i.field_name}"] [data-fieldname="${i.field_name}"]`).val()
                    }
                    if (i.field_type == "Select list (Single choice)" || i.field_type == "Radio Buttons"){
                        frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": `${type[i.field_type]}`,
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "options":`${i.options}`,
                                "reqd": i.reqd
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                    }
                    if (i.field_type == "User Picker (Single User)"){
                        frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": "Link",
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "reqd": i.reqd,
                                "options":"User"
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                    }
                    if (i.field_type == "Group Picker (single group)"){
                        frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": "Link",
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "reqd": i.reqd,
                                "options":"User Group"
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                    }
                    if (i.field_type == "User Picker (Multiple Users)"){
                        let input1 = frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": "Table MultiSelect",
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "reqd": i.reqd,
                                "options": "User Member",
                                "onchange": function() {
                                    let val = this.get_value();
                                },
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                    }
                    if (i.field_type == "Group Picker (multiple groups)"){
                        let input2 = frappe.ui.form.make_control({
                            parent: cur_frm.fields_dict.issue_screen_html.$wrapper,
                            df: {
                                "fieldtype": "Table MultiSelect",
                                "label": __(`${i.field_label}`),
                                "fieldname": `${i.field_name}`,
                                "reqd": i.reqd,
                                "options": "User Group Member"
                            },
                            render_input:true
                        })
                        $(`div[data-fieldname="${i.field_name}"]`).addClass('col-sm-4')
                    }
                    
                }
                frm.refresh_field("issue_screen_html")

            }
            else{
                frappe.throw({  title: __('Message'),
                                indicator: 'red',
                                message: __(res.message)
                            });
            }
        }
    })
}


frappe.ui.form.on("Bug Sheet", "validate", function(frm) {
    var data = frappe.datetime.now_date();
    if (frm.doc.status == "Fixed") {
        cur_frm.set_value("fixed_on", data);
    } else if (frm.doc.status == "Verified") {
        cur_frm.set_value("verified_on", data);
    }
});


frappe.ui.form.on("Bug Sheet", "assign", function(frm) {
    var arr = frm.doc.table_11;
    for (var i = 0; i < arr.length; i++) {
        $.ajax({
            url: window.location.origin + "/api/resource/DocShare",
            dataType: 'text',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "user": arr[i].assign_to,
                "share_doctype": frm.doc.doctype,
                "share_name": frm.doc.name,
                "read": 1,
                "write": 1,
                "share": 1
            }),
            beforeSend: function(xhr) {
                xhr.setRequestHeader(
                    'X-Frappe-CSRF-Token', frappe.csrf_token
                );
            },
            success: function(data) {
                console.log(data);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }
});