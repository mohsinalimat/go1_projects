// Copyright (c) 2024, Tridots Tech and contributors
// For license information, please see license.txt

frappe.query_reports["Task Summary"] = {
	"filters": [
		{
			label:"Project",
			fieldname:"name",
			fieldtype:"Link",
			options:"Project"
		},
		{
			label:"Milestone Task",
			fieldname:"milestone_task",
			fieldtype:"Check"
		}
	]
};
