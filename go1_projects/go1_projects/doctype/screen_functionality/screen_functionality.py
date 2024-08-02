# -*- coding: utf-8 -*-
# Copyright (c) 2018, Valiant Systems  and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ScreenFunctionality(Document):
	pass
	def before_insert(self):
		self.parental_task = frappe.db.get_value('Screen', self.screen, 'task')

		new_task = frappe.get_doc({
			"doctype": "Task",
			"subject": self.subject,
			"status": self.status,
			"project": self.project,
			"parent_task": self.parental_task,
			"is_group": 1
		})
		new_task.insert()
		self.db_set("task", new_task.name)

		for task in self.get('checkpoints'):
			chidltask = frappe.get_doc({
				"doctype": "Task",
				"subject": task.subject,
				"status": task.status,
				"project": self.project,
				"parent_task": self.task
			})
			chidltask.insert()	
			task.db_set("task", chidltask.name)


	def on_update(self):
		self.parental_task = frappe.db.get_value('Screen', self.screen, 'task')
		if not self.task:
			new_task = frappe.get_doc({
				"doctype": "Task",
				"subject": self.subject,
				"status": self.status,
				"project": self.project,
				"parent_task": self.parental_task,
				"is_group": 1
			})
			new_task.insert()	
			self.db_set("task", new_task.name)

		elif self.task:
			parent_task_parent = frappe.get_doc('Task', self.task)
			parent_task_parent.subject = self.subject
			parent_task_parent.status = self.status
			parent_task_parent.project = self.project
			parent_task_parent.is_group = 1
			parent_task_parent.parent_task = self.parental_task	
			parent_task_parent.save()		

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


