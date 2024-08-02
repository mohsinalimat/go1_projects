# Copyright (c) 2024, Tridots Tech and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today

def execute(filters=None):
	if not filters:filters={}
	columns=get_column()
	cs_data = get_data(filters)
	data =[]
	for d in cs_data:
		row ={
			"emp_id":f"<a href='/app/employee/{d['employee']}'><b>{d['employee_name']}</b> - <b>{d['employee']}</b></a>",
			# "emp_name":f"<b>{d['employee_name']}</b>",
			"indent":0
		}
		data.append(row)
		for t in d["tasks"]:
			task_row = {
				"project_name":t["project_name"],
				"task":t["subject"],
				"description":t["description"],
				"expected_hrs":t["expected_hrs"],
				"actual_hrs":t["actual_hrs"],
				"indent":1,
			}
			data.append(task_row)
	# return columns, data
	return columns , data


def get_column():
	return[
		{
			"fieldname":"emp_id",
			"label":"Employee Id",
			"fieldtype":"Data",
			# "options":"Employee",
			"width":"275"
		},
		# {
		# 	"fieldname":"emp_name",
		# 	"label":"Employee Name",
		# 	"fieldtype":"Data",
		# 	"width":"250"
		# },
		{
			"fieldname":"project_name",
			"label":"Project Name",
			"fieldtype":"Data",
			"width":"250"
		},
		{
			"fieldname":"task",
			"label":"Task",
			"fieldtype":"Data",
			"width":"250"
		},
		{
			"fieldname":"description",
			"label":"Description",
			"fieldtype":"Small Text",
			"width":"250"
		},
		{
			"fieldname":"expected_hrs",
			"label":"Expected Hours",
			"fieldtype":"Float",
			"width":"150"
		},
		{
			"fieldname":"actual_hrs",
			"label":"Actual Hours",
			"fieldtype":"Float",
			"width":"150"
		},
	]

def get_data(filters):
	log_list = frappe.get_all("Daily Update Log",
						   {"date":filters.get("date") if filters.get("date") else today()},
						   ['name',"employee"])
	data =[]
	for i in log_list:
		task_dict={}
		log_dict={"employee":i['employee'],"tasks":[]}
		log_dict['employee_name']=frappe.db.get_value("Employee",{"employee":i['employee']},'employee_name')
		table_data = frappe.get_all("Daily Update Log Item",filters = {"parent":i['name']},
							  fields=['project_name','subject','description','expected_hrs',"actual_hrs"])
		log_dict["tasks"]=table_data
		data.append(log_dict)
	# frappe.log_error("report data",data)
	return data