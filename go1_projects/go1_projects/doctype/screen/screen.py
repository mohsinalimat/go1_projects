# -*- coding: utf-8 -*-
# Copyright (c) 2017, Valiant Systems  and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Screen(Document):
	pass

	def on_update(self):
		pass
		# self.parental_task = frappe.db.get_value('Module', self.module, 'task')
	
		# parent_task = frappe.get_doc({
		# 	"doctype": "Task",
		# 	"subject": self.screen_name,
		# 	"status": self.status,
		# 	"project": self.project,
		# 	"parent_task": self.parental_task,
		# 	"is_group": 1
		# })
		# parent_task.insert()	
		# frappe.db.commit()
		# self.db_set("task", parent_task.name)
		
		# devo_task = frappe.get_doc({
		# 	"doctype": "Task",
		# 	"subject": self.screen_name+"(Development)",
		# 	"project": self.project,
		# 	"parent_task": self.task,
		# 	"is_group": 1
		# })
		# devo_task.insert()
		# frappe.db.commit()
		# self.db_set("development_task", devo_task.name)
		
		# testing_task = frappe.get_doc({
		# 	"doctype": "Task",
		# 	"subject": self.screen_name+"(Testing)",
		# 	"project": self.project,
		# 	"parent_task": self.task,
		# 	"is_group": 1
		# })
		# testing_task.insert()
		# frappe.db.commit()
		# self.db_set("testing_task", testing_task.name)

		# elif self.task:
		# 	parent_task = frappe.get_doc('Task', self.task)
		# 	parent_task.subject = self.screen_name
		# 	parent_task.status = self.status
		# 	parent_task.project = self.project
		# 	parent_task.parent_task = self.parental_task
		# 	parent_task.is_group = 1	
		# 	parent_task.save()	
