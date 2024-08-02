frappe.ui.form.on("Issue Type", {
	refresh(frm) {
        frm.add_custom_button("Add / Edit Workflow",() => {
            frappe.set_route("workflow-builder",frm.doc.issue_type_workflow)
        })
        frappe.call({
            method:"go1_projects.go1_projects.api.get_default_workflow",
            callback: function(r){
                console.log("RRRRR == ",r.message);
            }
        })
	},
    after_save: function (frm) {
        cur_frm.reload_doc()
    }
});