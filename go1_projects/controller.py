from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, cstr
from frappe.email.doctype.email_group.email_group import add_subscribers
from frappe.utils import (add_days, getdate, formatdate, date_diff, formatdate,
	add_years, get_timestamp, nowdate, flt, add_months, get_last_day)


@frappe.whitelist()
def senddailytask(allow_guest=True):	
	projects = frappe.db.get_list("Project", 
					fields=['project_name', 'status', 'name', 'priority'],
					filters={'status': "Open"},
					limit_page_length=200
					)	

	for x in projects:
		opentasks = frappe.db.get_list("Task", 
							fields=['name'],
							filters={'project': x.name, 'status': ["!=", "Closed"]},
							limit_page_length=200
							)
		if opentasks: 
			x.opentasks = len(opentasks)
		else:
			x.opentasks = 0	

		closedtasks = frappe.db.get_list("Task", 
							fields=['name'],
							filters={'project': x.name, 'status': 'Closed'},
							limit_page_length=200
							)
		if closedtasks: 
			x.closedtasks = len(closedtasks)
		else:
			x.closedtasks = 0	
		
		openbugs = frappe.db.get_list("Bug Sheet", 
							fields=['name'],
							filters={'project': x.name, 'status': ["in", "Closed"]},
							limit_page_length=200
							)
		if openbugs: 
			x.openbugs = len(openbugs)
		else:
			x.openbugs = 0	

		
		closedbugs = frappe.db.get_list("Bug Sheet", 
							fields=['name'],
							filters={'project': x.name, 'status': 'Closed'},
							limit_page_length=200
							)
		if closedbugs: 
			x.closedbugs = len(closedbugs)
		else:
			x.closedbugs = 0	

	table = '<table cellpadding="5" style="border-collapse: collapse;" border="1"><tr><th>Project Name</th><th>Open Tasks</th><th>Closed Tasks</th><th>Open Bugs</th><th>Closed Bugs</th></tr>'
	for y in projects:
		table = table + '<tr><td>'+str(y.project_name)+'</td><td>'+str(y.opentasks)+'</td><td>'+str(y.closedtasks)+'</td><td>'+str(y.openbugs)+'</td><td>'+str(y.closedbugs)+'</td></tr>'

	table = table + '</table>'	
	data = 'Daily Project summary @ '+formatdate(nowdate(), "dd-MM-yyyy")


	frappe.sendmail(recipients=['vigneshwaran@valiantsystems.com'],
		sender = "Testing Valiant2 <testing.valiant2@gmail.com>",
		message=table,
		subject=data)
	return None



@frappe.whitelist()
def senddailytimesheet(allow_guest=True):	
	google = '<div style="border: 1px solid black; "> <img src="https://cdn-images-1.medium.com/max/1200/0*pAdZLfSqNrMZAAPA.jpg" \
	alt="Avatar" style="width:70px; border-radius: 50%; float:left; padding-right: 23px; padding-left: 14px; padding-top: 8px;"> \
	<h4><b>John Doe</b></h4> <p>Architect & Engineer</p> </div><div style="border: 1px solid black;"> \
	<div class="m_8588087096502089317header-section" style="box-sizing:border-box;margin:0;padding:0">\
	 <div class="m_8588087096502089317logo-container" style="box-sizing:border-box;text-align:left;display:inline-block;width:40%;margin:0; padding-left: 45px" align="left">\
	  <p style="box-sizing:border-box;font-weight:normal;line-height:1.6;font-size:20px;color:#4a4a4c;margin:0 0 13.33333px;padding:0">\
	  <strong style="box-sizing:border-box;margin:0;padding:0"><span style="text-transform:uppercase;color:#141c3a;box-sizing:border-box;margin:0;padding:0">Task Title</span>\
	  </strong></p> </div> <div class="m_8588087096502089317newsletter-info" style="margin-left: 15px !important; box-sizing:border-box;float:right;text-align:right;margin:0;" align="right">\
	   <p style="background-color: #e44646; box-sizing:border-box;font-weight:normal;line-height:1.6;font-size:14px;color:#4a4a4c;margin:0 0 13.33333px;padding:5px;"><strong style="box-sizing:border-box;margin:0;padding:0"><span style="text-transform:uppercase;color:#141c3a;box-sizing:border-box;margin:0;padding:0">Status</span></strong></p> </div> <div class="m_8588087096502089317newsletter-info" style="box-sizing:border-box;float:right;text-align:right;margin:0;" align="right"> <p style="background-color: #e44646; box-sizing:border-box;font-weight:normal;line-height:1.6;font-size:14px;color:#4a4a4c;margin:0 0 13.33333px;padding:5px;"><strong style="box-sizing:border-box;margin:0;padding:0"><span style="text-transform:uppercase;color:#141c3a;box-sizing:border-box;margin:0;padding:0">Status</span></strong></p> </div> </div><div id="m_8588087096502089317main-story-2" style="box-sizing:border-box;margin:0;padding:0px 48px"> <p style="box-sizing:border-box;font-weight:normal;line-height:1.6;font-size:14px;color:#4a4a4c;margin:0 0 13.33333px;padding:0">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.</p> </div> </div><div style="border: 1px solid black;"> <h3 style="text-align: right; margin-right: 20px;">Total Working Hours : 9</h3> </div> </div>'
	Employee = frappe.db.get_list("Employee", 
					fields=['employee_name', 'name'],
					filters={'status': "Active"},
					limit_page_length=200
					)	
	table = '<table cellpadding="5" style="border-collapse: collapse;" border="1"><tr><th>Employee Name</th><th>Project</th><th>Task</th><th>Task Description</th><th>status</th><th>Total Hours</th></tr>'

	for x in Employee:
		x.Timesheet = frappe.db.get_list("Timesheet", 
							fields=['name','total_hours'],
							filters={'employee': x.name, 'start_date': ["=", nowdate()]},
							limit_page_length=200
							)

		for y in x.Timesheet:
			y.tasks = frappe.db.get_list("Timesheet Detail", 
								fields=['name', 'project', 'task', 'hours', 'from_time', 'to_time'],
								filters={'parent': y.name},
								limit_page_length=200
								)
			for q in y.tasks:
				q.tasks_details = frappe.db.get_list("Task", 
							fields=['subject', 'status', 'priority', 'description', 'name', 'project'],
							filters={'name': q.task},
							limit_page_length=200
							)
	

	for e in Employee:
		tar = ''
		for x in e.Timesheet:
			for y in x.tasks:
				if y.tasks_details[0].description:
					va = y.tasks_details[0].description
				else:
					va = "none"	

				if tar == '':	
					table += "<tr><td>"+str(e.employee_name)+"</td><td>"+y.tasks_details[0].project+"</td><td>"+str(y.tasks_details[0].subject)+"</td><td>"\
						 +str(va)+"</td><td>"+y.tasks_details[0].status+"</td><td>"+str(y.hours)+"</td></tr>"
					
					tar = e.employee_name 
				else: 
					table += "<tr><td></td><td>"+y.tasks_details[0].project+"</td><td>"+str(y.tasks_details[0].subject)+"</td><td>"\
						 +str(va)+"</td><td>"+y.tasks_details[0].status+"</td><td>"+str(y.hours)+"</td></tr>"	 
			    	


	table += "</table>"			
	
	data = 'Daily task summary @ '+formatdate(nowdate(), "dd-MM-yyyy")

	frappe.sendmail(recipients=['vigneshwaran@valiantsystems.com'],
		sender = "Testing Valiant2 <testing.valiant2@gmail.com>",
		message=google,
		subject=data)

	return Employee
















