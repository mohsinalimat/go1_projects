// Copyright (c) 2018, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on('Proposal Template', {
	refresh: function(frm) {

	}
});



frappe.ui.form.on("Proposal Child", "qty", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "rate", d.qty * d.price);

}); 	

frappe.ui.form.on("Proposal Child", "price", function (frm, cdt, cdn) {
	var d = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "rate", d.qty * d.price);

});