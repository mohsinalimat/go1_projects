// Copyright (c) 2024, Valiant Systems  and contributors
// For license information, please see license.txt

frappe.ui.form.on("Issue Custom Fields", {
	refresh(frm) {
		$('[data-fieldname="option_html"]').attr("style","display: flex;width: 100%;flex-wrap: wrap;")
		$('[data-fieldname="__column_2"]').attr("style","padding:0px !important")
		$('[data-fieldname="option_html"]').html("")
		
		frm.json = frm.doc.option_json ? JSON.parse(frm.doc.option_json) : []
		if(frm.doc.option_json){
			frm.values = frm.doc.options.split('\n');
			for(let jos of JSON.parse(frm.doc.option_json)){
				if(frm.values.includes(jos.field_name)){
					if (frm.doc.field_type == "Select list (Cascading)") {
						// frm.add_child("cascading_options",{
						// 	"parent_option": jos.field_name
						// })
						// frm.refresh_field("cascading_options")
						// frappe.ui.form.make_control({
						// 	parent: cur_frm.fields_dict.option_html.$wrapper,
						// 	df: {
						// 		"fieldtype": `Small Text`,
						// 		"label": __(`Options (${jos.field_name})`),
						// 		"fieldname": `${jos.field_name}`
						// 	},
						// 	render_input:true,
						// 	value:jos.value
						// })
						// $(`div[data-fieldname="${jos.field_name}"]`).addClass('col-sm-4')
					}
				}
			}
		}
		var input = document.querySelectorAll('textarea[data-fieldname="options"]')
		input[0].addEventListener("keyup", function(event) {
		
		
		
				if (frm.doc.options) {
				if (frm.doc.field_type == "Select list (Cascading)") {
					setTimeout(() => {
						let node_list = []
						frm.values = frm.doc.options.split('\n');
						for(let j of frm.doc.cascading_options){
							node_list.push(j.parent_option)
						}
						
						if (event.key === "Backspace") {
							for(let i = 0; i < frm.doc.cascading_options.length; i++){
								if(!frm.values.includes(frm.doc.cascading_options[i].parent_option)){
									cur_frm.get_field("cascading_options").grid.grid_rows[i].remove();
									cur_frm.refresh_field("cascading_options");
								}
							}
							
							
						}
						if (event.key === "Delete") {
							for(let i = 0; i < frm.doc.cascading_options.length; i++){
								if(!frm.values.includes(frm.doc.cascading_options[i].parent_option)){
									cur_frm.get_field("cascading_options").grid.grid_rows[i].remove();
									cur_frm.refresh_field("cascading_options");
								}
							}
						}

						if (event.key === "Enter") {
							for(let i = 0; i < frm.values.length; i++) {
								if(frm.values[i] !== '') {
									if(!node_list.includes(frm.values[i])){
										frm.add_child("cascading_options",{
											"parent_option": frm.values[i]
										})
										frm.refresh_field("cascading_options")
										
									}
									
								}
							}
						}
						$('[data-fieldname="cascading_options"] [class="row-check sortable-handle col"]').css("display","none")
						$('[data-fieldname="cascading_options"] [class="btn-open-row"]').parent().remove()
						$('[data-fieldname="cascading_options"] [class="col grid-static-col d-flex justify-content-center"]').remove()
						$('[data-fieldname="cascading_options"] [class="small form-clickable-section grid-footer"]').remove()
					},500)
				}
			};
		})
		
		
	},
	before_save(frm) {
		if (frm.doc.field_label){
			frm.doc.field_name = convertLabelToVariable(frm.doc.field_label)
		}
	},
	options:function(frm){
		setTimeout(() => {
			$('[data-fieldname="cascading_options"] [class="row-check sortable-handle col"]').css("display","none")
			$('[data-fieldname="cascading_options"] [class="btn-open-row"]').parent().remove()
			$('[data-fieldname="cascading_options"] [class="col grid-static-col d-flex justify-content-center"]').remove()
			$('[data-fieldname="cascading_options"] [class="small form-clickable-section grid-footer"]').remove()
		}, 100);
		
	},
	field_type(){
			$('[data-fieldname="cascading_options"] [class="row-check sortable-handle col"]').css("display","none")
			$('[data-fieldname="cascading_options"] [class="btn-open-row"]').parent().remove()
			$('[data-fieldname="cascading_options"] [class="col grid-static-col d-flex justify-content-center"]').remove()
			$('[data-fieldname="cascading_options"] [class="small form-clickable-section grid-footer"]').remove()
	}
});
frappe.ui.form.on("Cascading Options", {
    cascading_options_remove(){
			$('[data-fieldname="cascading_options"] [class="row-check sortable-handle col"]').css("display","none")
			$('[data-fieldname="cascading_options"] [class="btn-open-row"]').parent().remove()
			$('[data-fieldname="cascading_options"] [class="col grid-static-col d-flex justify-content-center"]').remove()
			$('[data-fieldname="cascading_options"] [class="small form-clickable-section grid-footer"]').remove()
		
    },
    cascading_options_add(){
			$('[data-fieldname="cascading_options"] [class="row-check sortable-handle col"]').css("display","none")
			$('[data-fieldname="cascading_options"] [class="btn-open-row"]').parent().remove()
			$('[data-fieldname="cascading_options"] [class="col grid-static-col d-flex justify-content-center"]').remove()
			$('[data-fieldname="cascading_options"] [class="small form-clickable-section grid-footer"]').remove()
		
    }
})
function convertLabelToVariable(label) {
	const cleanedLabel = label.replace(/[^a-zA-Z0-9]/g, '');
	const lowercaseLabel = cleanedLabel.toLowerCase();
	const variableName = lowercaseLabel.replace(/\s+/g, '_');
	return variableName;
}

