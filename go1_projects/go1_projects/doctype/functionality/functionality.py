# -*- coding: utf-8 -*-
# Copyright (c) 2018, Valiant Systems  and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document
from frappe.share import add
from frappe import _, throw

class Functionality(Document):
	def before_insert(self):
		if self.screen and self.module:
			self.parental_task = frappe.db.get_value('Screen', self.screen, 'development_task')
		elif self.module:
			self.parental_task = frappe.db.get_value('Module', self.module, 'task')	

		new_task = frappe.get_doc({
			"doctype": "Task",
			"subject": self.subject,
			"status": self.status,
			"project": self.project,
			"parent_task": self.parental_task,
			"description": self.description,
			"is_group": 1
		})
		new_task.insert()
		self.db_set("task", new_task.name)

	def on_update(self):
		
		if not self.task:
			if self.screen and self.module:
				self.parental_task = frappe.db.get_value('Screen', self.screen, 'development_task')
			elif self.module:
				self.parental_task = frappe.db.get_value('Module', self.module, 'task')	

			new_task = frappe.get_doc({
				"doctype": "Task",
				"subject": self.subject,
				"status": self.status,
				"project": self.project,
				"parent_task": self.parental_task,
				"description": self.description,
				"is_group": 1
			})
			new_task.insert()
			self.db_set("task", new_task.name)

		elif self.task:	
			if self.screen and self.module:
				self.parental_task = frappe.db.get_value('Screen', self.screen, 'development_task')
			elif self.module:
				self.parental_task = frappe.db.get_value('Module', self.module, 'task')	

			task = frappe.get_doc('Task', self.task)
			task.subject = self.subject
			task.status = self.status
			task.project = self.project
			task.parent_task = self.parental_task
			task.description = self.description
			task.save()

		for task in self.get('checkpoints'):
			if not task.task:
				chidltask = frappe.get_doc({
					"doctype": "Task",
					"subject": task.subject,
					"status": task.status,
					"project": self.project,
					"parent_task": self.task
				})
				chidltask.insert()	
				task.db_set("task", chidltask.name)

			elif task.task:
				chidltask = frappe.get_doc('Task', task.task)
				chidltask.subject = task.subject
				chidltask.status = task.status
				chidltask.project = self.project
				chidltask.parent_task = self.task
				chidltask.save()




