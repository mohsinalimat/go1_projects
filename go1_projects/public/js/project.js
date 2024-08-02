frappe.ui.form.on("Project", {
	refresh(frm) {
		// $('[class="transactions"]').find(".badge-link").filter(function() {
		//     return $(this).text().trim() === "Bug Sheet";
		// }).prop('outerHTML',"<a class=\"badge-link\">Issue</a>");
		// $('[data-fieldname="issue_type_screen_scheme"] [class="row-index sortable-handle col"]').css("display","none")
		
		$('[data-fieldname="issue_type_screen_scheme"] [class="row-check sortable-handle col"]').css("display","none")
		$('[data-fieldname="issue_type_screen_scheme"] [class="btn-open-row"]').parent().remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="col grid-static-col d-flex justify-content-center"]').remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="small form-clickable-section grid-footer"]').remove()
			
		
	},
	onload_post_render: function(frm) {
		frm.get_field("assign_roles").grid.set_multiple_add("user");
	},
	set_multiple_add(link, qty) {
		if (this.multiple_set) return;
 
		var link_field = frappe.meta.get_docfield(this.df.options, link);
		var btn = $(this.wrapper).find(".grid-add-multiple-rows");
 
		// show button
		btn.removeClass("hidden");
		this.grid_pagination = new GridPagination({
			grid: this,
			wrapper: this.wrapper,
		});
		// open link selector on click
		btn.on("click", () => {
			console.log("FFF");
			new frappe.ui.form.CustomLinkSelector({
				doctype: link_field.options,
				fieldname: link,
				qty_fieldname: qty,
				get_query: link_field.get_query,
				target: this,
				txt: "",
			});
			this.grid_pagination.go_to_last_page_to_add_row();
			return false;
		});
		this.multiple_set = true;
	},
	allowed_user: function(frm){
		let add_result = frm.doc.allowed_user.filter(aItem => !frm.doc.assign_roles.some(bItem => aItem.user === bItem.user));
		let remove_result = frm.doc.assign_roles.filter(aItem => !frm.doc.allowed_user.some(bItem => aItem.user === bItem.user));
		frm.add_child("assign_roles",{
			"user" : add_result[0].user
		})
		frm.refresh_field("assign_roles")
		if (remove_result.length !=0){
			cur_frm.get_field("assign_roles").grid.grid_rows[remove_result[0].idx-1].remove()
		}
	},
	custom_allowed_issue_type: function(frm){
		let add_result = frm.doc.custom_allowed_issue_type.filter(aItem => !frm.doc.issue_type_screen_scheme.some(bItem => aItem.issue_type === bItem.issue_type));
		let remove_result = frm.doc.issue_type_screen_scheme.filter(aItem => !frm.doc.custom_allowed_issue_type.some(bItem => aItem.issue_type === bItem.issue_type));

		if (add_result.length != 0){
			frappe.call({
				method:"go1_projects.go1_projects.api.set_issue_screening_workflows",
				args:{
					issue_type:add_result[0].issue_type
				},
				async:false,
				callback:function(r){
					frm.add_child("issue_type_screen_scheme",{
						"issue_type" : add_result[0].issue_type,
						"issue_type_screen":r.message.issue_type_screening,
						"edit_issue_type_screen":r.message.issue_type_screening,
						"issue_type_workflow":r.message.issue_type_workflow
					})
					frm.refresh_field("issue_type_screen_scheme")
				}
			})
		}
		
		if (remove_result.length !=0){
			cur_frm.get_field("issue_type_screen_scheme").grid.grid_rows[remove_result[0].idx-1].remove()
		}
		frm.refresh_field("issue_type_screen_scheme")
		$('[data-fieldname="issue_type_screen_scheme"] [class="row-check sortable-handle col"]').css("display","none")
		$('[data-fieldname="issue_type_screen_scheme"] [class="btn-open-row"]').parent().remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="col grid-static-col d-flex justify-content-center"]').remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="small form-clickable-section grid-footer"]').remove()
		
	}
});
frappe.ui.form.on("Issue Type Screening Scheme", {
	issue_type_screen_scheme_add(){
		$('[data-fieldname="issue_type_screen_scheme"] [class="row-check sortable-handle col"]').css("display","none")
		$('[data-fieldname="issue_type_screen_scheme"] [class="btn-open-row"]').parent().remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="col grid-static-col d-flex justify-content-center"]').remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="small form-clickable-section grid-footer"]').remove()
	},
	issue_type_screen_scheme_remove(){
		$('[data-fieldname="issue_type_screen_scheme"] [class="row-check sortable-handle col"]').css("display","none")
		$('[data-fieldname="issue_type_screen_scheme"] [class="btn-open-row"]').parent().remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="col grid-static-col d-flex justify-content-center"]').remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="small form-clickable-section grid-footer"]').remove()
	}
	
})
frappe.ui.form.on("Project Role Details", {
	assign_roles_add(frm,cdt,cdn){
		let d = locals[cdt][cdn]
		if(frm.doc.assign_roles.length > 1){

			for (let i=0;i<frm.doc.assign_roles.length-1;i++){
				if (d.user == frm.doc.assign_roles[i].user){
					cur_frm.get_field("assign_roles").grid.grid_rows[d.idx-1].remove()
				}	
			}
		}
		frm.refresh_field("issue_type_screen_scheme")
		$('[data-fieldname="issue_type_screen_scheme"] [class="row-check sortable-handle col"]').css("display","none")
		$('[data-fieldname="issue_type_screen_scheme"] [class="btn-open-row"]').parent().remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="col grid-static-col d-flex justify-content-center"]').remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="small form-clickable-section grid-footer"]').remove()
	},
	assign_roles_remove(){
		$('[data-fieldname="issue_type_screen_scheme"] [class="row-check sortable-handle col"]').css("display","none")
		$('[data-fieldname="issue_type_screen_scheme"] [class="btn-open-row"]').parent().remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="col grid-static-col d-flex justify-content-center"]').remove()
		$('[data-fieldname="issue_type_screen_scheme"] [class="small form-clickable-section grid-footer"]').remove()
	}
	
})
