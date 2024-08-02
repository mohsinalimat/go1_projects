# Copyright (c) 2024, Tridots Tech and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	proj_data = get_data(filters)
	# frappe.log_error("task filter",filters)
	milestone_filter = filters.get("milestone_task")
	project_filter = filters.get("name")
	 
	for i in proj_data:
		project_name = i["project"].split(" - ")
		project_data = data.append({"project":f"<a href='/project/{project_name[0]}'><b>{i['project']} (Total - {i['task_count']})</b></a>","indent":0})
		if (not milestone_filter) and (not project_filter):
			project_data
		else:
			if not milestone_filter:
				project_data
				for t in i["tasks"]:
					t["indent"] = 1
					data.append(t)
		# else:

		if milestone_filter:
			if i["milestone_tasks"]:
				for m in i["milestone_tasks"]:
					# frappe.log_error("ddddd",m["milestone"])
					data.append({
						"project":f"<b>{m['milestone']} (Total : {len(m['mile_tasks'])})</b>",
						# "name":f"<b>{len(m['mile_tasks'])}</b>",
						"indent":1
					})
					total=0
					for mt in m["mile_tasks"]:
						# frappe.log_error(f"{m['milestone']} count",len(m["mile_tasks"]))
						total+=1
						data.append({
							"name":mt["task_id"],
							"subject":mt["subject"],
							"status":mt["status"],
							"priority":mt["priority"],
							"exp_start_date":mt["exp_start_date"],
							"exp_end_date":mt["exp_end_date"],
							"indent":2
						})
						
			else:
				data.append({
					"project":"No milestone wise task"
				})
	columns = get_columns()
	# if milestone_filter:
	# 	mile_col={
	# 		"fieldname":"milestone",
	# 		"fieldtype":"Data",
	# 		"label":"Milestone",
	# 		"width":145,
	# 	}
	# 	columns.insert(1,mile_col)
	return columns, data

def get_columns():
	return [
		{"fieldname":"project","fieldtype":"Data","label":_("Project"),"options":"Project","width":300},
		{"fieldname": "name", "fieldtype": "Link", "label": _("Task"), "options": "Task", "width": 150},
		{"fieldname": "subject", "fieldtype": "Data", "label": _("Subject"), "width": 200},
		{"fieldname": "status", "fieldtype": "Data", "label": _("Status"), "width": 100},
		{"fieldname": "priority", "fieldtype": "Data", "label": _("Priority"), "width": 80},
		{"fieldname": "progress", "fieldtype": "Data", "label": _("Progress (%)"), "width": 120},
		{
			"fieldname": "exp_start_date",
			"fieldtype": "Date",
			"label": _("Expected Start Date"),
			"width": 150,
		},
		{
			"fieldname": "exp_end_date",
			"fieldtype": "Date",
			"label": _("Expected End Date"),
			"width": 150,
		},
		{"fieldname": "completed_on", "fieldtype": "Date", "label": _("Actual End Date"), "width": 130},
	]

def get_data(filters):
	data=[]
	applied_filters={}
	conditions = get_conditions(filters)
	# frappe.log_error("cond",filters)
	if filters.get("name"):
		applied_filters["name"] = filters.get("name")
	project = frappe.get_all(
		"Project",
		filters=applied_filters,
		fields=[
			"name",
			"project_name"
		]
	)
	for p in project:
		proj={"project":f"{p['name']} - {p['project_name']}"}
		conditions["project"]=p["name"]
		# frappe.log_error("conditions filters",conditions)
		tasks = frappe.get_all(
			"Task",
			filters=conditions,
			fields=[
				"name",
				"subject",
				"exp_start_date",
				"exp_end_date",
				"status",
				"priority",
				"completed_on",
				"progress",
			],
			order_by="creation",
		)
		task_count=frappe.get_all(
			"Task",
			filters=conditions,
			fields=[
				"COUNT(name) as task_count"
			]
		)
		proj["task_count"]=task_count[0]["task_count"]
		milestone_stmt = """
					SELECT t.name,t.subject,t.description,t.exp_end_date from tabTask t 
						WHERE t.is_milestone = 1 
							AND 
						t.is_group = 1 
							AND
						t.project = %(project)s
		"""
		milestone = frappe.db.sql(milestone_stmt,{"project":p["name"]},as_dict = 1)
		# frappe.log_error("proj milestones",milestone)
		mile_task_dicts=[]
		for d in milestone:
			task_stmt = """SELECT t.name,t.description,t.subject,t.status,t.exp_start_date,t.exp_end_date,t.priority
			  FROM tabTask t Where t.parent_task=%(parent_task)s"""
			mile_tasks = frappe.db.sql(task_stmt,{"parent_task":d["name"]},as_dict=True)
			# frappe.log_error("mile tasks",mile_tasks)
			each_milestone = {"milestone":d["subject"],"mile_tasks":[]}
			if mile_tasks:
				for t in mile_tasks:
					each_milestone["mile_tasks"].append({"task_id":t["name"],"subject":t["subject"],
										  "description":t["description"],"status":t["status"],"exp_start_date":t["exp_start_date"],
										  "exp_end_date":t["exp_end_date"],"priority":t["priority"]})
				mile_task_dicts.append(each_milestone)
		proj["milestone_tasks"] = mile_task_dicts if mile_task_dicts else []
		proj["tasks"]=tasks
		data.append(proj)
		# frappe.log_error(p["name"],tasks)
	# frappe.log_error("data",data)
	return data

def get_conditions(filters):
	conditions = frappe._dict()
	keys = ["priority", "status"]
	for key in keys:
		if filters.get(key):
			conditions[key] = filters.get(key)
	if filters.get("from_date"):
		conditions.exp_end_date = [">=", filters.get("from_date")]
	if filters.get("to_date"):
		conditions.exp_start_date = ["<=", filters.get("to_date")]
	return conditions