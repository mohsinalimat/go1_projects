# Copyright (c) 2024, info@tridotstech.com and contributors
# For license information, please see license.txt

import frappe,pymsteams
from frappe import _
from frappe.model.document import Document
from frappe.utils import today,getdate,get_datetime
from bs4 import BeautifulSoup
import re

class DailyUpdate(Document):
	
	@frappe.whitelist()
	def fetch_pending_tasks(self):
		if frappe.db.exists("Daily Update Log",{"date":self.start_date,"user":frappe.session.user}):
			return ""
		cur_year = getdate().year
		start_date=f"{cur_year}-01-01"
		# frappe.log_error("start_date",getdate().year)
		tasks = frappe.get_list("Task",filters={"status":['not in',['Completed']],'exp_start_date':['between',[start_date,today()]]},fields=['name',"subject",'description','expected_time','project'])
		# frappe.log_error("self tasks",tasks)
		for i in tasks:
			if i.description:
				if bool(re.search(r'<[^>]+>', i.description)):
					soup = BeautifulSoup(i.description, 'html.parser')
					i.description = soup.get_text(strip=True)
		return tasks
	
	@frappe.whitelist()
	def send_update(self):
		exist= frappe.db.exists("Daily Update Log",{"date":self.start_date,"user":frappe.session.user})
		if exist:
			frappe.log_error("creating timesheet")
			return self.trigger_update_and_timesheet()
		else:
			frappe.log_error("creating log")
			return self.enqueue_update_create_log()

	@frappe.whitelist()
	def log_exists(self):
		exist= frappe.db.exists("Daily Update Log",{"date":self.start_date,"user":frappe.session.user})
		if not exist:
			return ""
		return "log"
	
	@frappe.whitelist()
	def enqueue_update_create_log(self):
		frappe.enqueue(self.send_update_create_log,queue="long")
		return "Create Log Success"

	@frappe.whitelist()
	def send_update_create_log(self):
		try:
			work_items=[{"user":frappe.session.user,"tasks":[]}]
			exists = frappe.db.exists("Daily Update Log",{"date":self.start_date,"user":frappe.session.user})
			# frappe.log_error("exists",exists)
			if exists:
				doc= frappe.get_doc("Daily Update Log",exists)
			else:
				doc = frappe.new_doc("Daily Update Log")
				doc.employee = frappe.db.get_value("Employee",{"user_id":frappe.session.user},['name'])
				doc.user = frappe.session.user
			
			if self.allocate_task:
				for i in self.allocate_task:
					work_items[0]['tasks'].append(i)
					doc.append("work_item",{
						"project":frappe.db.get_value("Task",{'name':i.task},['project']),
						"project_name":frappe.db.get_value("Project",
										 {"name":frappe.db.get_value("Task",{'name':i.task},['project'])},
										 ['project_name']),
						"task":i.task,
						"description":i.description if i.description else "",
						"subject":i.subject,
						"expected_hrs":i.expected_hours
					})
					if (not frappe.db.get_value("Task",{"name":i.task},['exp_start_date']))\
						  and frappe.db.get_value("Task",{"name":i.task},['expected_time']) == 0:
						frappe.db.set_value("Task",i.task,{
							"exp_start_date":self.start_date,
							"expected_time":i.expected_hours
						})
					else:
						cur_time = float(frappe.db.get_value("Task",{'name':i.task},['expected_time']))
						frappe.db.set_value("Task",i.task,"expected_time",float(cur_time+i.expected_hours))
						# frappe.log_error("setting value","set")
					# if frappe.db.get_value("Task",{'name':i.task},['exp_start_date']) and frappe.db.get_value("Task",{"name":i.task},['expected_time']) > 0:
						
					# 	# frappe.log_error("updating time",float(cur_time+i.expected_hours))
			
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
						tasks_txt+=f"{idx}. [{i.subject}]({link}) expected hours: {i.expected_hours}\r"
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
					doc.save(ignore_permissions = True)
					teams_message.send()

				
		except Exception:
			frappe.log_error("Exception arises sending update",frappe.get_traceback())

	
	# def create_update_log(self):
	# 	emp = frappe.db.get

	
	
	@frappe.whitelist()
	def get_my_works(self):
		if frappe.db.exists("Daily Update Log",{"date":self.start_date,"user":frappe.session.user}):
			my_tasks = frappe.get_doc("Daily Update Log",{"date":self.start_date,"user":frappe.session.user})
			return my_tasks.work_item
		
	@frappe.whitelist()
	def get_task_description(self,args):
		task_description = frappe.db.get_value("Task",args.task,
										 ['subject','description',
										'project','expected_time','project'])
		description=''
		if task_description[1]:
			if bool(re.search(r'<[^>]+>', task_description[1])):
				soup = BeautifulSoup(task_description[1], 'html.parser')
				description = soup.get_text(strip=True)
		# frappe.log_error("task desc",frappe.db.get_value("Task",args.task,['subject','description']))
		return [task_description[0],description,
		  task_description[2],task_description[3],task_description[4]]
	
	#Completed.....
	@frappe.whitelist()
	def update_my_log(self):
		if frappe.db.exists("Daily Update Log",{"date":self.start_date,"user":frappe.session.user}):
			my_tasks = frappe.get_doc("Daily Update Log",{"date":self.start_date,"user":frappe.session.user})
			my_tasks.work_item=[]
			for i in self.allocate_task:
				self.validate_overlap(i)
				# frappe.log_error("expec",i.actual_hrs)
				my_tasks.append("work_item",{
					"project":i.project,
					"project_name":frappe.db.get_value("Project",{'name':i.project},['project_name']) if i.project else "",
					"task":i.task,
					"subject":i.subject,
					"description":i.description if i.description else "",
					"expected_hrs":i.expected_hours,
					"from_time":i.from_time_update,
					"to_time":i.to_time,
					"started":i.started,
					"completed":i.completed,
					"actual_hrs":i.actual_hours,
					"status":i.status if i.status else "",
					"activity":i.activity
				})
			my_tasks.save(ignore_permissions = True)

	@frappe.whitelist()
	def trigger_update_and_timesheet(self):
		frappe.enqueue(self.send_update_create_timesheet,queue="long")
		return "assigned"
	
	@frappe.whitelist()
	def send_update_create_timesheet(self):
		try:
			
			employee=frappe.db.get_value("Employee",{"user_id":frappe.session.user},['employee',"employee_name"])
			exists = frappe.db.exists("Timesheet",{"employee":employee[0],"start_date":self.start_date,"end_date":self.start_date})
			if exists:
				tasks=[]
				employee=frappe.db.get_value("Employee",{"user_id":frappe.session.user},['employee',"employee_name"])
				doc = frappe.get_doc("Timesheet",exists)
				doc.time_logs=[]
				tasks_txt=""
				url =f'{frappe.utils.get_url()}'
				for i in self.allocate_task:
					# link=f"{url}/app/task/{i.task}"
					# # # frappe.log_error('links',link)
					# tasks_txt+=f"- [{i.subject}]({link})  \n**Working Hours:** {i.expected_hours}\n **status**:{i.status}\r"
					# # idx+=1
					doc.append("time_logs",{
						"project":i.project,
						"task":i.task,
						# "hours":i.actual_hours,
						"activity_type":i.activity,
						"from_time":i.from_time_update,
						"to_time":i.to_time
					})
					if i.status == "Completed":
						frappe.db.set_value("Task",i.task,{
							"status":i.status,
							"completed_on":self.start_date
						})
					else:
						frappe.db.set_value("Task",i.task,"status",i.status)
				stmt = f""" SELECT DT.task ,DT.subject ,DT.description, DT.status,SUM(DT.actual_hrs) as actual_hrs 
							From `tabDaily Update Log` DU 
								Inner Join 
							`tabDaily Update Log Item` DT on DT.parent = DU.name 
							Where date = "{self.start_date}" And user = "{frappe.session.user}" Group by DT.task"""
				cumulative_task = frappe.db.sql(stmt,as_dict = True)
				# frappe.log_error("Cumulative",cumulative_task)
				for i in cumulative_task:
					link=f"{url}/app/task/{i.task}"
					# # frappe.log_error('links',link)
					task_status = frappe.db.get_value("Task",i.task,'status')
					tasks_txt+=f"- [{i.subject}]({link})  \n**Working Hours:** {round(i.actual_hrs, 3)}\n **status**:{task_status}\r"

				user_group = frappe.db.get_value("Teams Webhook",{"user":frappe.session.user},'webhook_url')
				teams_message = pymsteams.connectorcard(user_group)
				content = {"type": "AdaptiveCard",
							"body": [
								{
									"type": "Container",
									"items": [
										{
											"type": "TextBlock",
											"text": f"Today's Update {today()}",
											"weight": "bolder",
											"size": "large"
										},
										# 
										{
											"type": "TextBlock",
											"text": f"Employee Id : {employee[0]}"
										},
										{
											"type": "TextBlock",
											"text": f"Employee Name : {employee[1]}",
											
										},
										{
											"type":"TextBlock",
											"text":"Tasks",
											"weight": "bolder",
											"size": "large"
										},
										{
											"type":"Container",
											"items":[
												{
													"type":"TextBlock",
													"text": f"{tasks_txt}",
													"wrap":True
												}
											]
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
				doc.save(ignore_permissions = True)
				teams_message.send()

			else:
				tasks=[]
				doc=frappe.new_doc("Timesheet")
				employee=frappe.db.get_value("Employee",{"user_id":frappe.session.user},['employee',"employee_name"])
				idx = 1
				doc.employee = employee[0]
				tasks_txt=""
				url =f'{frappe.utils.get_url()}'
			
				for i in self.allocate_task:
					if i.status == "Completed":
						frappe.db.set_value("Task",i.task,{
							"status":i.status,
							"completed_on":self.start_date
						})
						frappe.db.set_value("ToDo",
						  {"reference_type":"Task","reference_name":i.task,"allocated_to":frappe.session.user},"status","Closed")
					else:
						frappe.db.set_value("Task",i.task,"status",i.status)
					
					doc.append("time_logs",{
						"project":i.project,
						"task":i.task,
						"hours":i.actual_hours,
						"activity_type":i.activity,
						"from_time":i.from_time_update,
						"to_time":i.to_time
					})

				stmt = f""" SELECT DT.task ,DT.subject ,DT.description, DT.status,SUM(DT.actual_hrs) as actual_hrs 
							From `tabDaily Update Log` DU 
								Inner Join 
							`tabDaily Update Log Item` DT on DT.parent = DU.name 
							Where date = "{self.start_date}" And user = "{frappe.session.user}" Group by DT.task"""
				cumulative_task = frappe.db.sql(stmt,as_dict = True)
				# frappe.log_error("Cumulative",cumulative_task)
				for i in cumulative_task:
					link=f"{url}/app/task/{i.task}"
					# # frappe.log_error('links',link)
					task_status = frappe.db.get_value("Task",i.task,'status')
					tasks_txt+=f"- [{i.subject}]({link})  \n**Working Hours:** {round(i.actual_hrs, 3)}\n **status**:{task_status}\r"
				
				user_group = frappe.db.get_value("Teams Webhook",{"user":frappe.session.user},'webhook_url')
				teams_message = pymsteams.connectorcard(user_group)
				content = {"type": "AdaptiveCard",
							"body": [
								{
									"type": "Container",
									"items": [
										{
											"type": "TextBlock",
											"text": f"Today's Update {today()}",
											"weight": "bolder",
											"size": "large"
										},
										# 
										{
											"type": "TextBlock",
											"text": f"Employee Id : {employee[0]}"
										},
										{
											"type": "TextBlock",
											"text": f"Employee Name : {employee[1]}",
											
										},
										{
											"type":"TextBlock",
											"text":"Tasks",
											"weight": "bolder",
											"size": "large"
										},
										{
											"type":"Container",
											"items":[
												{
													"type":"TextBlock",
													"text": f"{tasks_txt}",
													"wrap":True
												}
											]
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
				
				doc.save(ignore_permissions = True)
				teams_message.send()
		except Exception:
			frappe.log_error("timesheet update error",frappe.get_traceback())

	@frappe.whitelist()
	def get_task_details(self,args):
		data =  frappe.get_doc("Task",{"name":args.task},["subject","project","description"])
		if data.description:
			if bool(re.search(r'<[^>]+>', data.description)):
				soup = BeautifulSoup(data.description, 'html.parser')
				data.description = soup.get_text(strip=True)
		return data
		
	def validate_overlap(self,args):
		timesheet = frappe.qb.DocType("Timesheet")
		timelog = frappe.qb.DocType("Timesheet Detail")

		from_time = get_datetime(args.from_time_update)
		to_time = get_datetime(args.to_time)
		existing = (
			frappe.qb.from_(timesheet)
			.join(timelog)
			.on(timelog.parent == timesheet.name)
			.select(
				timesheet.name.as_("name"), timelog.from_time.as_("from_time"), timelog.to_time.as_("to_time")
			)
			.where(
				(timelog.name != (args.name or "No Name"))
				& (timesheet.name != (args.parent or "No Name"))
				& (timesheet.docstatus < 2)
				& (
					((from_time > timelog.from_time) & (from_time < timelog.to_time))
					| ((to_time > timelog.from_time) & (to_time < timelog.to_time))
					| ((from_time <= timelog.from_time) & (to_time >= timelog.to_time))
				)
			)
		).run(as_dict=True)
		if existing:
			frappe.throw(
				_("Row {0}: From Time and To Time of your update is overlapping with Timesheet {1}").format(
					args.idx,existing[0].name
				),
			)
		self_existing = self.check_internal_overlap(args)
		if self_existing:
			frappe.throw(
				_("Row {0}: From Time and To Time of your update is overlapping").format(
					args.idx,
				),
			)

	def check_internal_overlap(self, args):
		for time_log in self.allocate_task:
			if not (time_log.from_time_update and time_log.to_time and args.from_time_update and args.to_time):
				continue

			from_time = get_datetime(time_log.from_time_update)
			to_time = get_datetime(time_log.to_time)
			args_from_time = get_datetime(args.from_time_update)
			args_to_time = get_datetime(args.to_time)

			if (
				(args.idx != time_log.idx)
				and (
					(args_from_time > from_time and args_from_time < to_time)
					or (args_to_time > from_time and args_to_time < to_time)
					or (args_from_time <= from_time and args_to_time >= to_time)
				)
			):
				return True
		return False
@frappe.whitelist()
def get_popup_query(doctype, txt , searchfield, start, page_len, filters):
	conditions=[]
	# frappe.log_error("filter",filters)
	for key,value in filters.items():
		if type(filters.get(key) == list):
			conditions.append([key,filters.get(key)[0],filters.get(key)[1]])
		else:
			conditions.append(key,value)
	data = frappe.get_list("Task",filters=conditions,fields=["name","subject","description"])
	# frappe.log_error("dt",data)

	for i in data:
		if i.description:
			if bool(re.search(r'<[^>]+>', i.description)):
				soup = BeautifulSoup(i.description, 'html.parser')
				i.description = soup.get_text(strip=True)
	# return 
	return data
