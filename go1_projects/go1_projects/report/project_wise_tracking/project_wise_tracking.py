# Copyright (c) 2024, Tridots Tech and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_column()
	data=[]
	cs_data = get_data(filters)
	for d in cs_data:
		pr_row={
			"project":f"<a href='/app//project/{d['project']}'><b>{d['project_name']} - {d['project']}</b></a>",
			"total_tasks":d["total_tasks"],
			"indent":0
		}
		data.append(pr_row)
		if d["milestone"]:
			for t in d["milestone"]:
				row={
					"milestone":t["subject"],
					"no_of_tasks":t["no_of_tasks"],
					"completed_tasks":t["completed"],
					"pending_tasks":t["pending"],
					"status":f"{int(t['status'])}%",
					"exp_end_date":t["exp_end_date"],
					"indent":1
				}
				data.append(row)
				# for mt in t["mile_tasks"]:
				# 	mt_row={
				# 		"task":mt["task_id"],
				# 		"subject":mt["subject"],
				# 		"description":mt["description"],
				# 		"status":mt["status"],
				# 		"indent":2
				# 	}
				# 	data.append(mt_row)
		else:
			row={
					"milestone":"No milestone tasks",
					"no_of_tasks":"",
					"completed_tasks":"",
					"pending_tasks":"",
					"status":"",
					"exp_end_date":"",
					"indent":1
			}
			data.append(row)

	return columns, data

def get_column():
	return[
		{
			"fieldname":"project",
			"label":"Project",
			"fieldtype":"Data",
			"width":"250"
		},
		{
			"fieldname":"total_tasks",
			"label":"Total Tasks",
			"fieldtype":"Int",
			"width":"100"
		},
		{
			"fieldname":"milestone",
			"label":"Milestone",
			"fieldtype":"Data",
			"width":"250"
		},
		{
			"fieldname":"status",
			"label":"Status",
			"fieldtype":"Data",
			"width":"100"
		},
		# {
		# 	"fieldname":"task",
		# 	"label":"Task",
		# 	"fieldtype":"Data",
		# 	"width":"250"
		# },
		# {
		# 	"fieldname":"subject",
		# 	"label":"Subject",
		# 	"fieldtype":"Data",
		# 	"width":"250"
		# },
		# {
		# 	"fieldname":"description",
		# 	"label":"Description",
		# 	"fieldtype":"Small Text",
		# 	"width":"250"
		# },
		
		{
			"fieldname":"no_of_tasks",
			"label":"No.of Tasks",
			"fieldtype":"Int",
			"width":"100"
		},
		{
			"fieldname":"completed_tasks",
			"label":"Completed Tasks",
			"fieldtype":"Int",
			"width":"100"
		},
		{
			"fieldname":"pending_tasks",
			"label":"Pending Tasks",
			"fieldtype":"Int",
			"width":"100"
		},
		# {
		# 	"fieldname":"status",
		# 	"label":"Status",
		# 	"fieldtype":"Data",
		# 	"width":"100"
		# },
		{
			"fieldname":"exp_end_date",
			"label":"Expected End Date",
			"fieldtype":"Date",
			"width":"150"
		},
		{
			"fieldname":"comments",
			"label":"Comments",
			"fieldtype":"Data",
			"width":"250"
		}

	]

def get_data(filters):
	project_list = frappe.get_all("Project")
	data=[]
	if not filters.get("project"):
		for i in project_list:
			create_data(data,i['name'])
	else:
		create_data(data,filters.get("project"))
	return data

def create_data(data,project):
	milestone_dict={"project":project,"project_name":frappe.db.get_value("Project",project,["project_name"]),"milestone":[]}
	milestone_stmt = """
					SELECT t.name,t.subject,t.description,t.exp_end_date from tabTask t 
						WHERE t.is_milestone = 1 
							AND 
						t.is_group = 1 
							AND
						t.project = %(project)s
	"""
	mile_data =frappe.db.sql(milestone_stmt,{"project":project},as_dict=True)
	pr_task = frappe.db.sql(""" SELECT Count(t.name) as pr_count from tabTask t 
							Where t.project=%(project)s""",{"project":project},as_dict=True)
	# frappe.log_error("mile data",mile_data)
	milestone_dict["total_tasks"] = pr_task[0]["pr_count"]
	for d in mile_data:
		stmt="SELECT Count(t.name)as task_count from tabTask t Where t.parent_task = %(parent)s"
		t_count = frappe.db.sql(stmt,{"parent":d["name"]},as_dict=True)
		
		t_completed = frappe.db.sql(stmt+" AND t.status = 'Completed'",{"parent":d["name"]},as_dict=True)
		pending = t_count[0]["task_count"]-t_completed[0]["task_count"]
		status = ((t_completed[0]["task_count"])/(t_count[0]["task_count"]))*100
		
		#Testing milestone tasks
		task_stmt = """SELECT t.name,t.description,t.subject,t.status from tabTask t Where t.parent_task=%(parent_task)s"""
		mile_tasks = frappe.db.sql(task_stmt,{"parent_task":d["name"]},as_dict=True)
		# frappe.log_error("mile tasks",mile_tasks)
		# mile_task_dicts=[]
		# for t in mile_tasks:
		# 	mile_task_dicts.append({"task_id":t["name"],"subject":t["subject"],"description":t["description"],"status":t["status"]})
		milestone_dict['milestone'].append({"task":d["name"],"subject":d["subject"],"completed":t_completed[0]["task_count"],
										"no_of_tasks":t_count[0]["task_count"],"status":status if status else 0,
										"comments":d["description"] if d["description"] else "","pending":pending,
										"exp_end_date":d["exp_end_date"],})
		# "mile_tasks":mile_task_dicts
	data.append(milestone_dict)