# -*- coding: utf-8 -*-
# Copyright (c) 2017, Valiant Systems  and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe.share import add
from frappe import _, throw

class BugSheet(Document):
	@frappe.whitelist()
	def get_issue_type_screening(self,flag = 0):
		if frappe.db.exists("Issue Type Screening",{"name":self.issue_type}):
			issue_type = frappe.db.get_value("Issue Type Screening Scheme",{"parent":self.project,"issue_type":self.issue_type},["issue_type_screen","edit_issue_type_screen"],as_dict = 1)
			filters = {}
			if not flag:
				if not self.is_new():
					if issue_type.issue_type_screen == issue_type.edit_issue_type_screen:
						filters = {"parent": issue_type.issue_type_screen}
					else:
						filters = {"parent": ["IN",[issue_type.issue_type_screen,issue_type.edit_issue_type_screen]]}
				else:
					filters = {"parent": issue_type.issue_type_screen}
					
			if flag == 1:
				if not self.is_new():
					if issue_type.issue_type_screen == issue_type.edit_issue_type_screen:
						filters = {"parent": issue_type.issue_type_screen}
					else:
						filters = {"parent": ["IN",[issue_type.issue_type_screen,issue_type.edit_issue_type_screen]]}
				else:
					filters = {"parent": issue_type.issue_type_screen}
			doc = frappe.db.get_all(
				"Issue Type Screening Details",
				fields = ["field_label"],
				filters = filters,
				order_by = "idx"
				)
			if doc:
				doc_list = []
				for i in doc:
					field_doc = frappe.db.get_value("Issue Custom Fields",i.field_label,["field_label","field_type","field_name","reqd","options"],as_dict = 1)
					doc_list.append(field_doc)
				return 	{	"status":"Success",
							"message" :doc_list
						}
			else:
				frappe.log_error("Error in get_issue_type_screening",frappe.get_traceback())
				return 	{	"status":"Failed",	
							"message" :"Issue Type Screening Details is Missing"
						}
		else:
			frappe.log_error("Error in get_issue_type_screening",frappe.get_traceback())
			return 	{	"status":"Failed",
						"message" :"Issue Type Screening is Missing"
					}

	@frappe.whitelist()
	def get_workflow_action(self):
		issue_type = frappe.db.get_value("Issue Type Screening Scheme",{"parent":self.project,"issue_type":self.issue_type},["issue_type_workflow"])
		filters = {"parent":issue_type,"state":self.status}
		query=	f"""SELECT role FROM `tabProject Role Details` 
					WHERE parent = '{self.project}'
					AND user='{frappe.session.user}' 
					ORDER BY idx ASC
				"""
		get_roles = frappe.db.sql(query,as_dict=1)
		frappe.log_error("get_rolesget_roles",get_roles)
		if get_roles:
			filters["allowed"]= ["IN",[i.role for i in get_roles]]
			frappe.log_error("FILTERS",filters)
			data = frappe.db.get_all("Workflow Transition",filters=filters,fields=["state","action","next_state","allowed"])
			return data
	
	@frappe.whitelist()
	def get_first_state(self):
		issue_type = frappe.db.get_value("Issue Type Screening Scheme",{"parent":self.project,"issue_type":self.issue_type},["issue_type_workflow"])
		state = frappe.db.get_value("Workflow Document State",{"parent":issue_type,"idx":1},["state"])
		return state


@frappe.whitelist()
def get_users(names):

	names = json.loads(names)
	name = tuple(names)
	params = {'l': name}
	projects = frappe.db.sql('''select distinct project from `tabBug Sheet` where name in %(l)s''',params)
	projects = tuple(projects)
	params1 = {'u': projects}
	users = frappe.db.sql('''select distinct user from `tabDocShare` where share_name in %(u)s''',params1)
	
	return users
	

@frappe.whitelist()
def post(user, doctype, names):
	names = json.loads(names)
	users = json.loads(user)
	for x in users:
		if x[1] == 1:
			for name in names:
				add(doctype, name, user=x[0], read=1, write=1, share=0, everyone=0, flags=None, notify=0)
	return users

@frappe.whitelist()
def get_tree_data():
	
	projects = frappe.db.get_list('Project',fields=['Project_name','name'])

	modules = frappe.db.get_list('Module',fields=['project','module_name','name'])

	screens = frappe.db.get_list('Screen',fields=['screen_name','project','module','name'])

	bugs = frappe.db.get_list('Bug Sheet',fields=['bug_title','project','module','screen','name'])
	

	for x in projects:
		x.type = 'projects'
		x.open = checkopen(x,modules,screens,bugs)

	for x in modules:
		x.type = 'modules'
		x.open = checkopen(x,modules,screens,bugs)

	for x in screens:
		x.type = 'screens'
		x.open = checkopen(x,modules,screens,bugs)

	for x in bugs:
		x.type = 'bugs'
		x.open = checkopen(x,modules,screens,bugs)
	
	return {'projects':projects, 'modules':modules, 'screens':screens, 'bugs':bugs}


def checkopen(i,modules,screens,bugs):
	quan = 'false'
	if i.type == 'projects':
		for x in modules:
			if i.name == x.project:
				quan = 'true'

	if i.type == 'modules':
		for x in screens:
			if i.name == x.module:
				quan = 'true'

	if i.type == 'screens':
		for x in bugs:
			if i.name == x.screen:
				quan = 'true'

	if i.type == 'bugs':
		quan = None

	return quan		


@frappe.whitelist()
def get_allowed_issue_types(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(f"""SELECT issue_type FROM `tabProject Issue Type`
								 WHERE parent='{filters.get("project")}'
							""")







