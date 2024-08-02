# -*- coding: utf-8 -*-
# Copyright (c) 2018, Valiant Systems  and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words,nowdate
from frappe.model.naming import make_autoname
from frappe.utils import random_string

class Proposal(WebsiteGenerator):
	def validate(self):
		if not self.route and self.is_published:
			self.route = 'proposal/'+random_string(15)
		
	def autoname(self):
		self.name = make_autoname('Proposal.#####')

	def on_update(self):
		if self.route:
			pass
		elif self.route == None and self.is_published:
			self.route = 'proposal/'+random_string(15)



@frappe.whitelist()
def sendaccmail(id, location):
	frappe.db.set_value("Proposal", id, "status", "Accept")
	data = frappe.db.get_single_value('Proposal Settings', 'acceptance_mail_template')
	proposals = frappe.db.get_list('Proposal',
		fields = ["title", "client_email", "client_name", "status", "route", "subject", "grand_total","route"],
		filters = {'name': ["=", id]},
		order_by = "idx")[0]	

	tot = str(proposals.grand_total)
	to_admin = "Hi<br>Client "+proposals.client_name+" accepted the following proposal:<br>\
                Subject: "+proposals.title+"<br>\
				Total: "+tot+"<br>\
				View the proposal on the following link: <a href="+location+">"+proposals.title+"</a><br>\
				Kind regards,<br>\
				Admin,<br>\
				Tridots Tech Pvt Ltd.,"

	to_client = "Hi "+proposals.client_name+",<br>\
				"+data+"<br>\
				Kind regards,<br>\
				Tridots Tech Pvt Ltd.,"				
	
	frappe.sendmail(recipients=["vigneshwaran@valiantsystems.com"],
	message= to_admin,
	subject= "Customer Accepted Proposal")


	frappe.sendmail(recipients=[proposals.client_email],
	message= to_client,
	subject= proposals.subject)
	
	return data		
		
@frappe.whitelist()
def sendrejmail(id, location):
	frappe.db.set_value("Proposal", id, "status", "Reject")
	data = frappe.db.get_single_value('Proposal Settings', 'rejection_mail_template')
	proposals = frappe.db.get_list('Proposal',
		fields = ["title", "client_email", "client_name", "status", "symbol", "route", "subject", "grand_total","route"],
		filters = {'name': ["=", id]},
		order_by = "idx")[0]	

	tot = str(proposals.grand_total)

	to_client = "Hi "+proposals.client_name+",<br>\
				"+data+"<br>\
				Kind regards,<br>\
				Tridots Tech Pvt Ltd.,"				
	
	to_admin = "Hi<br>Client "+proposals.client_name+" rejected the following proposal:<br>\
                Subject: "+proposals.title+"<br>\
				Total: "+tot+"<br>\
				View the proposal on the following link: <a href="+location+">"+proposals.title+"</a><br>\
				Kind regards,<br>\
				Admin,<br>\
				Tridots Tech Pvt Ltd.,"
	
	frappe.sendmail(recipients=["vigneshwaran@valiantsystems.com"],
	message= to_admin,
	subject= "Customer Rejected Proposal")

	frappe.sendmail(recipients=[proposals.client_email],
	message= to_client,
	subject= proposals.subject)

	return to_admin	
	

@frappe.whitelist()
def get_data_from_template(template):
	data = frappe.db.get_list('Proposal Data',
			fields = ['title', 'content'],
			filters = {'parent': template},
			order_by = "idx")

	data1 = frappe.db.get_list('Proposal Samples',
			fields = ['image', 'url'],
			filters = {'parent': template},
			order_by = "idx")
	return data,data1

@frappe.whitelist()
def get_items_from_template(template,currency):
	data = frappe.db.get_list('Proposal Child',
			fields = ['item', 'description', 'price', 'qty', 'rate', 'currency'],
			filters = {'parent': template, 'currency': currency},
			order_by = "idx")

	return data

@frappe.whitelist()
def get_lead_details(lead):
	data = frappe.db.get_list('Lead',
			fields = ['lead_name', 'email_id', 'mobile_no'],
			filters = {'name': lead},
			order_by = "idx")

	return data[0]	


@frappe.whitelist()
def schedulemail():
	proposals = frappe.db.get_list('Proposal',
		fields = ["title", "client_email", "client_name", "status", "route", "subject"],
		filters = {'count': [">", 0], 'status': ["=", "Pending"]},
		or_filters={
		"second_notification_date": ("=", nowdate()),
		"third_notification_date": ("=", nowdate()),
		"fourth_notification_date": ("=", nowdate())
		},
		order_by = "idx")	


	body = frappe.db.get_single_value('Proposal Settings', 'ebody')
	s_name = frappe.db.get_single_value('Proposal Settings', 'sender_name')
	s_email = frappe.db.get_single_value('Proposal Settings', 'sender_email')
	if proposals:
		for x in proposals:
			
			frappe.sendmail(recipients=[x.client_email],
			sender = s_name+" <"+s_email+">",
			message= body,
			subject= x.subject)

	return proposals


@frappe.whitelist()
def sendproposalemail(route,title,email,body,cover,cname):
	data = "Proposal Web view : <a href="+route+">"+cover+"</a>"
	freq = frappe.db.get_single_value('Proposal Settings', 'email_interval_frequency')
	s_name = frappe.db.get_single_value('Proposal Settings', 'sender_name')
	s_email = frappe.db.get_single_value('Proposal Settings', 'sender_email')
	val = 'Dear'+' '+cname+','
	frappe.sendmail(recipients=[email],
		sender = s_name+" <"+s_email+">",
		message= val+'<br>'+body+ '<br>' +data,
		subject= title)

	return freq





















