// Copyright (c) 2024, Valiant Systems  and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Issue Type Screening", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Issue Type Screening Details", {
	field_label: function(frm,cdt,cdn) {
        var d = locals[cdt][cdn]
        frm.call({
            doc:frm.doc,
            method:"get_field_details",
            async:false,
            args:{name:d.field_label},
            callback:function(r){
               
                // frappe.model.set_value(cdt,cdn,"json",r.message)
            }
        })
        frm.refresh_field("fields")
	},
});

