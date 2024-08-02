// Copyright (c) 2024, Tridots Tech and contributors
// For license information, please see license.txt

frappe.query_reports["Project wise Tracking"] = {
	"filters": [
		{
			fieldname:"project",
			fieldtype:"Link",
			options:"Project",
			label:"Project"
		}
	]
};
