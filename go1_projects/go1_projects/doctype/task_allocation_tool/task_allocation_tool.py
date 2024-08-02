# Copyright (c) 2024, Valiant Systems  and contributors
# For license information, please see license.txt

import frappe,pymsteams,json
from datetime import datetime
from frappe.utils import today
from frappe.model.document import Document
from frappe.utils import getdate
from frappe.model.document import Document


class TaskAllocationTool(Document):
	def assign_tasks(self,args):
		# try:
			tasks=[]
			doclist= args.json
			# frappe.log_error("doclist",doclist['task'])
			for i in doclist['task']:
				flag = False
				if 'user' in i:
					if tasks:
						for t in tasks:
							if t['user'] == i['user']:
								t['tasks'].append({'id':i['task'],"subject":i['subject']})
								flag=True
								break
						if not flag:
							tasks.append({"user":i['user'],'tasks':[{'id':i['task'],'subject':i['subject']}]})
					else:
						tasks.append({"user":i['user'],'tasks':[{'id':i['task'],'subject':i['subject']}]})
				else:
					frappe.throw(f"Assign user for {i['task']}")

			# frappe.log_error("task",tasks)
			if tasks:
				for task in tasks:
					try:
						# frappe.log_error("cur_url",frappe.session.user)
						self.generate_message(task)
						self.create_todo(task)
					except Exception:
						frappe.log_error("error in sending message",frappe.get_traceback())
					
		# except Exception:
		# 	frappe.log_error("exception",frappe.get_traceback())

	@frappe.whitelist()
	def assign_tasks_enqueue(self,args):
		frappe.enqueue(self.assign_tasks,args=args,queue="long")
		return "allocated"
	

	@frappe.whitelist()
	def pending_task(self):
		query_stmt = """SELECT p.project_name,t.project,count(*) as count from `tabTask` t 
						LEFT JOIN `tabTask Allocated To` al ON al.parent=t.name 
						LEFT JOIN `tabProject` p ON t.project = p.name 
						WHERE al.user IS NULL AND t.is_group = 0 AND t.is_milestone = 0 GROUP BY t.project"""
		pending = frappe.db.sql(query_stmt,as_dict = True)
		# frappe.log_error("pedning",pending)
		return pending

	def generate_message(self,task):
		from frappe.utils import today
		from frappe.utils import cstr
		try:
			user_group = frappe.db.get_value("Teams Webhook",{"user":task['user']},'webhook_url')
			frappe.log_error("webhook url",user_group)
			if user_group:
				user_name = frappe.db.get_value("User",{"name":task['user']},['full_name'])
				teams_message = pymsteams.connectorcard(user_group)
				idx = 1
				tasks_txt=""
				url =f'{frappe.utils.get_url()}'
				for i in task['tasks']:
					# frappe.log_error("site",site_name)
					link=f"{url}/app/task/{i['id']}"
					# frappe.log_error('links',link)
					tasks_txt+=f"{idx}. [{i['subject']}]({link})\r"
					idx+=1
				# frappe.log_error("task",tasks_txt[0:-1])
				content = {"type": "AdaptiveCard",
					"body": [
						{
							"type": "Container",
							"items": [
								{
									"type": "TextBlock",
									"text": f"Task Allocation {today()}",#Task allocation title
									"weight": "bolder",
									"size": "large"
								},
								# 
								{
									"type": "TextBlock",
									"text": f"Hello <at>{task['user']}</at>" #Task allocation subject
								},
								{
									"type": "TextBlock",
									"text": tasks_txt,
									"wrap": True  
								}
							]
						}
					],
					# "msteams": {
					# 			"entities": [
					# 				{
					# 					"type": "mention",
					# 					"text": f"<at>{user_name}</at>",
					# 					"mentioned": {
					# 						"id": task['user'],
					# 						"name": user_name
					# 					}
					# 				}
					# 			]
                    #                 },
					"$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
					"version": "1.4"
				}
				teams_message.payload = {
						"type":"message",
						"attachments":[
							{
								"contentType":"application/vnd.microsoft.card.adaptive",
								"content":content
							}
						]
					}
			
				teams_message.send()
		except Exception:
			frappe.log_error("error in pymsteams",frappe.get_traceback())

	@frappe.whitelist()
	def create_todo(self,task):
		from bs4 import BeautifulSoup
		import re
		for i in task['tasks']:
			doc = frappe.new_doc("ToDo")
			text_content=''
			if frappe.db.get_value("Task",{"name":i['id']},['description']):
				if bool(re.search(r'<[^>]+>', frappe.db.get_value("Task",{"name":i['id']},['description']))):
					soup = BeautifulSoup(frappe.db.get_value("Task",{"name":i['id']},['description']), 
						  'html.parser')
					text_content = soup.get_text(strip=True)
			doc.description = text_content if text_content else f"Assignment for Task {i['id']}"
			doc.allocated_to=task['user']
			doc.reference_type = "Task"
			doc.reference_name = i['id']
			doc.date = ""
			doc.assigned_by = frappe.session.user
			doc.insert()
			share = frappe.new_doc("DocShare")
			share.share_name = i['id']
			share.share_doctype = "Task"
			share.user = task['user']
			share.read=1
			share.write=1
			share.insert()

			doc = frappe.get_doc("Task", i['id'])
			doc.append("custom_allocated_to",{
				'user':task['user']
			})
			doc.save()



	@frappe.whitelist()
	def get_task_description(self,args):
		return frappe.db.get_value("Task",args.task,'subject')
	
	@frappe.whitelist()
	def get_allocation_history(self):
		emp_tasks=[]
		today = datetime.today().date()
		today_str = today.strftime('%Y-%m-%d')
		user = frappe.session.user
		docs = frappe.get_list("ToDo",
						 filters={"assigned_by":user,"reference_type":"Task",
				"creation":['between',[today_str+" 00:00:00",today_str+" 23:59:59"]],"status":["!=","Cancelled"]},
				fields=['reference_name',"status","description","allocated_to","creation"])
		for i in docs:
			emp_id=frappe.db.get_value("Employee",{"user_id":i['allocated_to']})
			emp=frappe.db.get_value("Employee",{"user_id":i['allocated_to']},['employee_name'])
			status = frappe.db.get_value("Task",{'name':i['reference_name']},['status'])
			if emp_tasks:
				flag = False
				for e in emp_tasks:
					if e['name'] == (emp_id+" - "+emp):
						e['tasks'].append(
							{"proj":frappe.db.get_value("Task",{"name":i['reference_name']},'project'),
						 "task":i['reference_name'],"status":status,'desc':i['description']})
						flag = True
						break
				if not flag:
					emp_tasks.append({"name":emp_id+" - "+emp,
					   "tasks":[{"proj":frappe.db.get_value("Task",{"name":i['reference_name']},'project'),
				  "task":i['reference_name'],"status":status,'desc':i['description']}]})
			else:
				emp_tasks.append({"name":emp_id+" - "+emp,
					  "tasks":[{"proj":frappe.db.get_value("Task",{"name":i['reference_name']},'project'),
				 "task":i['reference_name'],"status":status,'desc':i['description']}]})
		# frappe.log_error("emp_tasks",emp_tasks)
		return emp_tasks
	
	@frappe.whitelist()
	def fetch_unallocated_tasks(self,args):
		unalloc_tasks=[]
		tasks=frappe.get_all("Task",{"project":args.project,"is_group":0,"is_milestone":0},['name','subject'])
		for i in tasks:
			alloc = frappe.get_all("Task Allocated To",{"parent":i['name']})
			if not alloc:
				unalloc_tasks.append(i)
		return unalloc_tasks
	
	@frappe.whitelist()
	def fetch_allocated_tasks(self):
		alloc_task=[]
		tasks=frappe.get_all("Task",{"project":self.project,"status":['not in',['Completed']]},['name','subject'])
		for i in tasks:
			alloc = frappe.get_all("Task Allocated To",filters={"parent":i['name']},fields=['user'])
			if alloc:
				user=""
				for a in alloc:
					user+=a['user']+","
				i['user']=user[:-1]
				# frappe.log_error("iii",i)
				alloc_task.append(i)
		# frappe.log_error("alloc",alloc_task)
		return alloc_task
	
	
	
	@frappe.whitelist()
	def send_update(self):
		try:
			work_items=[{"user":frappe.session.user,"tasks":[]}]
			for i in self.self_allocation_task:
				if(i.status == "Working"):
					work_items[0]['tasks'].append(i)
			user_group = frappe.db.get_value("Teams Webhook",{"user":work_items[0]['user']},'webhook_url')
			if user_group:
				teams_message = pymsteams.connectorcard(user_group)
				idx = 1
				tasks_txt=""
				url =f'{frappe.utils.get_url()}'
				for i in work_items[0]['tasks']:
					# frappe.log_error("iii",i.task)
					link=f"{url}/app/task/{i.task}"
					# # frappe.log_error('links',link)
					tasks_txt+=f"{idx}. [{i.subject}]({link})\r"
					idx+=1
				# frappe.log_error("task",tasks_txt)
				content = {"type": "AdaptiveCard",
					"body": [
						{
							"type": "Container",
							"items": [
								{
									"type": "TextBlock",
									"text": f"Today's Work Item {today()}",
									"weight": "bolder",
									"size": "large"
								},
								# 
								{
									"type": "TextBlock",
									"text": f"Following are the tasks going to work for today:"
								},
								{
									"type": "TextBlock",
									"text": tasks_txt,
									"wrap": True  
								}
							]
						}
					],
					"$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
					"version": "1.4"
				}
				teams_message.payload = {
						"type":"message",
						"attachments":[
							{
								"contentType":"application/vnd.microsoft.card.adaptive",
								"content":content
							}
						]
					}
				# frappe.log_error("content",content)
				teams_message.send()
		except Exception:
			frappe.log_error("Exception arises sending update",frappe.get_traceback())

		
