# Copyright (c) 2024, Valiant Systems  and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IssueTypeScreening(Document):
	@frappe.whitelist()
	def get_field_details(self,name):
		doc_json = frappe.db.get_all("Cascading Options",filters = {"parent":name},fields = ["parent_option","options"])
		return doc_json
		
