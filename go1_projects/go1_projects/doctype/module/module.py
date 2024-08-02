# -*- coding: utf-8 -*-
# Copyright (c) 2017, Valiant Systems  and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe.share import add
from frappe import _, throw

class Module(Document):
	pass

	# def before_insert(self):
	# 	parent_task = frappe.get_doc({
	# 		"doctype": "Task",
	# 		"subject": self.module_name,
	# 		"status": self.status,
	# 		"project": self.project,
	# 		"is_group": 1
	# 	})
	# 	parent_task.insert()
	# 	self.db_set("task", parent_task.name)

	# def on_update(self):
	# 	if not self.task:
	# 		parent_task = frappe.get_doc({
	# 			"doctype": "Task",
	# 			"subject": self.module_name,
	# 			"status": self.status,
	# 			"project": self.project,
	# 			"is_group": 1
	# 		})
	# 		parent_task.insert()	
	# 		self.db_set("task", parent_task.name)

	# 	elif self.task:
	# 		parent_task = frappe.get_doc('Task', self.task)
	# 		parent_task.subject = self.module_name
	# 		parent_task.status = self.status
	# 		parent_task.project = self.project
	# 		parent_task.is_group = 1	
	# 		parent_task.save()		




@frappe.whitelist()
def delete(project, module):
	frappe.db.sql("""DELETE FROM `tabModule Screen Child` where parent=%s""",(module))
	return 0

@frappe.whitelist()
def get_screens(project, module):
	data = frappe.db.sql("""SELECT screen_name FROM `tabScreen` WHERE project=%s AND module=%s""",(project, module))
	return data


