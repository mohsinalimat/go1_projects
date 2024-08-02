import frappe,json
from frappe.utils import today,flt
from datetime import datetime,timedelta, time
from frappe.utils.data import now_datetime
from frappe.utils import now
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def set_issue_screening_workflow(doc,method):
    if not doc.issue_type_screening:
        if not frappe.db.exists("Issue Type Screening",{"issue_type":doc.name}):
            screen = frappe.new_doc("Issue Type Screening")
            screen.issue_type = doc.name
            screen.insert(ignore_permissions = True)
            frappe.db.set_value("Issue Type",doc.name,"issue_type_screening",screen.name)
            frappe.db.commit()
        
    if not doc.issue_type_workflow:
        if not frappe.db.exists("Workflow",{"Workflow_name":doc.name}):
            default_workflow = frappe.db.get_single_value("Issue Type Settings","default_workflow")
            workflow = get_mapped_doc("Workflow", default_workflow, {
                "Workflow": {
                    "doctype": "Workflow",
                    "name": doc.name}
            })
            workflow.workflow_name = doc.name
            workflow.document_type = "Issue Type"
            workflow.insert(ignore_permissions = True)
            frappe.db.set_value("Issue Type",doc.name,"issue_type_workflow",workflow.name)
            frappe.db.commit()


@frappe.whitelist()
def set_issue_screening_workflows(issue_type):
    doc = frappe.db.get_value("Issue Type",{"name":issue_type},["issue_type_screening","issue_type_workflow"],as_dict = 1)
    return doc

@frappe.whitelist()
def get_default_workflow():
    doc = frappe.db.get_single_value("Issue Type Settings","default_workflow")
    return doc

#Daily Updates API
@frappe.whitelist()
def update_start_timer(task,time,activity):
    doc = frappe.get_doc("Daily Update Log",{'date':today(),'user':frappe.session.user})
    for i in doc.work_item:
        if i.task == task:
            i.started = 1
            i.from_time = time
            i.activity = activity
    doc.save(ignore_permissions = True)


@frappe.whitelist()
def update_end_timer(task,time,actual_hours):
    doc = frappe.get_doc("Daily Update Log",{'date':today(),'user':frappe.session.user})
    for i in doc.work_item:
        if (i.task == task )and (i.started) and (not i.completed):
            i.completed = 1
            i.to_time = time
            i.actual_hrs = actual_hours
    doc.save(ignore_permissions=True)
        
@frappe.whitelist()
def update_task_list(t,start_time,activity):
    doc = frappe.get_doc("Daily Update Log",{'date':today(),'user':frappe.session.user})
    frappe.log_error("task_lits_update",t)
    task_obj = json.loads(t)
    doc.append("work_item",{
        "task":task_obj['task'],
        "description":task_obj['description'],
        "expected_hrs":task_obj['expected_hours'],
        "started":1,
        "project":task_obj['project'],
        "subject":task_obj['subject'],
        "activity":activity,
        "from_time":start_time
    })
    doc.save(ignore_permissions = True)

@frappe.whitelist()
def cumulative_update_message(employee=None):
    # if not date:
    #     frappe.throw("Kindly set date to get update")
    du_setting = frappe.get_single("Daily Update Setting")
    filters={"date":du_setting.date if du_setting.date else today()}
    if employee:
        filters["employee"]=employee
    log_list = frappe.get_list("Daily Update Log",filters=filters,fields=['name','employee'])
    frappe.log_error("filters log",filters)
    # frappe.log_error("log list data",log_list)
    html_template_data = []
    for i in log_list:
        log_dict={}
        doc = frappe.get_list("Daily Update Log Item",{"parent":i.name},['*'])
        log_dict['emp_id']=i.employee
        log_dict['emp_name'] = frappe.db.get_value("Employee",{"employee":i.employee},'employee_name')
        stmt="""
                Select dut.project,dut.subject,dut.description,dut.expected_hrs,dut.actual_hrs from `tabDaily Update Log` du
                    Inner Join `tabDaily Update Log Item` dut
                    on dut.parent=%(parent)s 
                Where du.date = %(date)s Group by dut.task
                """
        emp_task = frappe.db.sql(stmt,{"parent":i.name,"date":du_setting.date if du_setting.date else today()},as_dict=True)
        if emp_task:
            log_dict['task']=emp_task
            html_template_data.append(log_dict)
            frappe.log_error("cumlulative log",html_template_data)
            if employee:
                # frappe.log_error("creating table if conditions")
                return create_html_table(html_template_data,employee)
    if not employee:
        # if type == "btn_click":
        create_html_table(html_template_data)
        # if (not type) and (du_setting.morning_daily_update_report):
        #     send_mail_time = datetime.strptime(du_setting.morning_daily_update_report,"%H:%M:%S").time()
        #     str_cur = now().split(".")[0]
        #     frappe.log_error("morning update type",type(send_mail_time))
        #     date_obj=datetime.strptime(str_cur,"%Y-%m-%d %H:%M:%S")
        #     cur_time = date_obj.time()
        #     if cur_time == send_mail_time:
        #         create_html_table(html_template_data)


def create_html_table(data,employee=None):
    html_table = """"""
    # flag =0
    for i in data:
        html_table+=f"""<p>{i['emp_id']} - <b>{i['emp_name']}</b></p>
        <table style="width:100%;border:1px solid black;border-collapse:collapse">
            <thead>
                <tr>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Project Name</th>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Task Subject</th>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Task Description</th>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Expected Hrs</th>
                </tr>
            </thead>
        <tbody>"""
        # task_count = len(i['task'])
        # html_table+=f"""<tr> 
        #                     <td style="font-size:13px;border:1px solid black">{i["emp_id"]}</td> 
        #                     <td style="font-size:13px;border:1px solid black">{i["emp_name"]}</td></tr
        for t in i['task']:
            html_table+=f"""
                <tr>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{frappe.db.get_value("Project",t["project"],'project_name') if t['project'] else ""}</td>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{t["subject"]}</td>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{t["description"]}</td>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{t["expected_hrs"]}</td>
                </tr>
            """
            # flag+=1
        html_table += """
            </tbody>
            </table>
            <br>
        """
    frappe.log_error("table design",html_table)
    if employee:
        return html_table
    send_mail(html_table)


@frappe.whitelist()
def cumulative_closing_update(employee=None):
    du_setting = frappe.get_single("Daily Update Setting")
    html_template_data = []
    filters={"date":du_setting.date if du_setting.date else today()}
    if employee:
        filters["employee"]=employee
    log_list = frappe.get_list("Daily Update Log",filters = filters,fields=['name','employee'])
    for i in log_list:
        log_dict={}
        doc = frappe.get_list("Daily Update Log Item",{"parent":i.name},['*'])
        log_dict['emp_id']=i.employee
        log_dict['emp_name'] = frappe.db.get_value("Employee",{"employee":i.employee},'employee_name')
        stmt="""
                    SELECT dut.project,dut.subject,dut.description,SUM(dut.actual_hrs) as actual_hrs , dut.expected_hrs from 
                    `tabDaily Update Log Item` dut
                    WHERE dut.parent=%(parent)s
                    GROUP BY dut.task
                """
        emp_task = frappe.db.sql(stmt,{"parent":i.name},as_dict=True)
        frappe.log_error("emp task",emp_task)
        log_dict['task']=emp_task
        html_template_data.append(log_dict)
    if employee:
        if html_template_data:
            frappe.log_error(employee,html_template_data)
            return create_closing_html_table(html_template_data,employee=employee)
        else:
            return 
    frappe.log_error("cumlulative log",html_template_data)
    create_closing_html_table(html_template_data)


def create_closing_html_table(data,employee=None):
    html_table = """"""
    # flag =0
    for i in data:
        html_table+=f"""<p>{i['emp_id']} - <b>{i['emp_name']}</b></p>
        <table style="width:100%;border:1px solid black;border-collapse:collapse">
            <thead>
                <tr>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Project Name</th>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Task Subject</th>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Task Description</th>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Expected Hrs</th>
                <th style="font-weight:600;font-size:13px;border:1px solid black">Actual Hrs</th>
                </tr>
            </thead>
        <tbody>"""
        for t in i['task']:
            html_table+=f"""
                <tr>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{frappe.db.get_value("Project",t["project"],'project_name') if t['project'] else ""}</td>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{t["subject"]}</td>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{t["description"]}</td>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{t["expected_hrs"]}</td>
                    <td style="font-weight:600;font-size:13px;border:1px solid black">{t["actual_hrs"]}</td>
                </tr>
            """
            # flag+=1
        html_table += """
            </tbody>
            </table>
            <br>
        """
    if employee:
        return html_table
    du_setting = frappe.get_single("Daily Update Setting")
    frappe.log_error("closing table design",html_table)
    send_mail(html_table,custom_subject=f" Closing Update Report {du_setting.date if du_setting.date else today()}")


def send_mail(data,recipients = None,custom_subject = None,update=None):
    try:
        du_setting = frappe.get_single("Daily Update Setting")
        recipient=[]
        subject =""
        if not recipients:
            for i in du_setting.recipient:
                recipient.append(i.user)
        # if update =="opening":
        if not custom_subject:
            subject = du_setting.subject if du_setting.subject else f"Daily Update Report {du_setting.date if du_setting.date else today()}"
        # if update == "closing":
        #     subject = du_setting.subject if du_setting.subject else f"Closing Update Report {du_setting.date if du_setting.date else today()}"
        frappe.log_error("subject",subject)
        frappe.log_error("recipients",recipient)
        if du_setting.date:
            doc = frappe.get_doc("Daily Update Setting","Daily Update Setting")
            doc.date = None
            frappe.log_error("du settign2222 di=ccc=csch",doc.as_dict())
            doc.save(ignore_permissions = True)
            frappe.db.commit()
        frappe.sendmail(recipients=recipient, subject=subject if not custom_subject else custom_subject, 
                        message=data)
    except Exception:
        frappe.log_error("Send Mail Error",frappe.get_traceback())

@frappe.whitelist()
def project_wise_tracking():
    project = frappe.get_list("Project")
    frappe.log_error("project",project)
    data=[]
    for i in project:
        milestone_dict={"project":i['name'],"project_name":frappe.db.get_value("Project",i['name'],["project_name"]),"milestone":[]}
        milestone_stmt = """
                        SELECT t.name,t.subject,t.description,t.exp_end_date from tabTask t 
                            WHERE t.is_milestone = 1 
                                AND 
                            t.is_group = 1 
                                AND
                            t.project = %(project)s
        """
        mile_data =frappe.db.sql(milestone_stmt,{"project":i["name"]},as_dict=True)
        pr_task = frappe.db.sql(""" SELECT Count(t.name) as pr_count from tabTask t 
                                Where t.project=%(project)s""",{"project":i["name"]},as_dict=True)
        frappe.log_error("mile data",mile_data)
        milestone_dict["total_tasks"] = pr_task[0]["pr_count"]
        for d in mile_data:
            # milestone_dict["exp_end_date"]=d["exp_end_date"]    
            stmt="SELECT Count(t.name)as task_count from tabTask t Where t.parent_task = %(parent)s"
            t_count = frappe.db.sql(stmt,{"parent":d["name"]},as_dict=True)
           
            t_completed = frappe.db.sql(stmt+" AND t.status = 'Completed'",{"parent":d["name"]},as_dict=True)
            pending = t_count[0]["task_count"]-t_completed[0]["task_count"]
            status = ((t_completed[0]["task_count"])/(t_count[0]["task_count"]))*100
            
            milestone_dict['milestone'].append({"task":d["name"],"subject":d["subject"],"completed":t_completed[0]["task_count"],
                                            "no_of_tasks":t_count[0]["task_count"],"status":status if status else 0,
                                            "comments":d["description"] if d["description"] else "","pending":pending,
                                            "exp_end_date":d["exp_end_date"]})
           
        data.append(milestone_dict)
    frappe.log_error("data",data)
    project_track_html(data)

def project_track_html(data):
    html=""
    for i in data:
        idx=1
        html+=f"""<p><b>{i["project_name"]}</b> - {i["project"]}</p>
                  <p>Total no.of tasks : {i["total_tasks"]}</p>
                <table style="width:100%;border:1px solid black;border-collapse:collapse;">
                      <thead>
                        <tr>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">S.No</th>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">Milestone</th>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">No.of tasks</th>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">Completed tasks</th>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">Pending tasks</th>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">Status</th>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">Expected End Date</th>
                        <th style="font-weight:600;font-size:13px;border:1px solid black">Comments</th>
                        </tr>
                    </thead>
                    <tbody>
            """
        frappe.log_error("milestone list",i["milestone"])
        if i["milestone"]:
            for t in i["milestone"]:
                html+=f"""
                        <tr>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{idx}</td>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{t["subject"]}</td>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{t["no_of_tasks"]}</td>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{t["completed"]}</td>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{t["pending"]}</td>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{int(t["status"])}%</td>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{t["exp_end_date"]}</td>
                            <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;">{t["comments"]}</td>
                        </tr>
                    """
                idx+=1
            html+="</tbody></table>"
        else:
           html+=f"""
                 <tr>
                    <td style="font-weight:600;font-size:13px;border:1px solid black;padding:10px;text-align:center;" colspan = "8">No milestone wise data</td>
                </tr>
                </tbody></table>
            """     
    frappe.log_error("pr table",html)

@frappe.whitelist()
def mail_reports_to():
    stmt="""SELECT e.reports_to from tabEmployee e Where e.reports_to is Not Null Group by e.reports_to """
    reports_to = frappe.db.sql(stmt,as_dict=1)
    for r in reports_to:
        html=""
        report_stmt="SELECT e.name,e.employee_name from tabEmployee e Where e.reports_to = %(report_to)s"
        report = frappe.db.sql(report_stmt,{"report_to":r["reports_to"]},as_dict=1)
        frappe.log_error("report to",report)
        # frappe.log_error("cumulative update log",cumulative_update_message("HR-EMP-00001"))
        if report:
            # frappe.log_error("inside if....")
            for i in report:
                # frappe.log_error("reportin name",i['name'])
                emp_data = cumulative_closing_update(employee=i["name"])
                frappe.log_error("emp dt type",type(emp_data))
                # frappe.log_error(f"emp data {frappe.db.get_value("Employee",{"name":i['name']},["employee_name"])}",emp_data)
                if emp_data:
                    frappe.log_error(frappe.db.get_value("Employee",{"name":r["reports_to"]},["employee_name"]),frappe.db.get_value("Employee",{"name":i["name"]},["employee_name"]))
                    # frappe.log_error(frappe.db.get_value("Employee",{"name":i['name']},["employee_name"]),html)
                    # nams.append(i["name"])
                    html+=emp_data
            if len(html)>0:
                du_setting = frappe.get_single("Daily Update Setting")
                frappe.log_error(frappe.db.get_value("Employee",{"name":r["reports_to"]},["employee_name"]),html)
                frappe.log_error("send mail",[frappe.db.get_value("Employee",{"name":r["reports_to"]},["employee_name"]),html])
                send_mail(html,recipients=frappe.db.get_value("Employee",{"name":r["reports_to"]},["user_id"]),custom_subject=f"Daily Update Report {du_setting.date if du_setting.date else today()}")