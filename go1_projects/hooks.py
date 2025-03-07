app_name = "go1_projects"
app_title = "Go1 Projects"
app_publisher = "Tridots Tech"
app_description = "App for managing projects"
app_email = "info@tridotstech.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

fixtures = ["Custom Field"]
# include js, css files in header of desk.html
# app_include_css = "/assets/go1_projects/css/go1_projects.css"
app_include_js = "/assets/go1_projects/js/update_timer.js"

# include js, css files in header of web template
# web_include_css = "/assets/go1_projects/css/go1_projects.css"
# web_include_js = "/assets/go1_projects/js/go1_projects.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "go1_projects/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_js = {
    "Issue Type" : "public/js/issue_type.js",
    "Project" : "public/js/project.js"
    }

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "go1_projects/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "go1_projects.utils.jinja_methods",
# 	"filters": "go1_projects.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "go1_projects.install.before_install"
# after_install = "go1_projects.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "go1_projects.uninstall.before_uninstall"
# after_uninstall = "go1_projects.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "go1_projects.utils.before_app_install"
# after_app_install = "go1_projects.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "go1_projects.utils.before_app_uninstall"
# after_app_uninstall = "go1_projects.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "go1_projects.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
	"Issue Type": {
		"on_update": "go1_projects.api.set_issue_screening_workflow"
	}
}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"go1_projects.tasks.all"
# 	],
# 	"daily": [
# 		"go1_projects.tasks.daily"
# 	],
# 	"hourly": [
# 		"go1_projects.tasks.hourly"
# 	],
# 	"weekly": [
# 		"go1_projects.tasks.weekly"
# 	],
# 	"monthly": [
# 		"go1_projects.tasks.monthly"
# 	],
# }
scheduler_events = {
# 	"all": [
# 		"pms.tasks.all"
# 	],
    "cron": {
        # "0/10 * * * *": [
        #     "library_management.task.run_every_ten_mins"
        # ],
        "30 19 * * *": [
            "go1_projects.go1_projects.doctype.proposal.proposal.schedulemail"
        ],
        "30 11 * * *":["go1_projects.api.cumulative_update_message",
                        "go1_projects.api.mail_reports_to"
        ],
        "00 22 * * *":[
            "go1_projects.api.cumulative_closing_update",
            "go1_projects.api.mail_reports_to"
        ]
    },
	"daily": [
		"go1_projects.controller.senddailytask"
	],
# 	"hourly": [
# 		"pms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pms.tasks.weekly"
# 	]
# 	"monthly": [
# 		"pms.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "go1_projects.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "go1_projects.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "go1_projects.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["go1_projects.utils.before_request"]
# after_request = ["go1_projects.utils.after_request"]

# Job Events
# ----------
# before_job = ["go1_projects.utils.before_job"]
# after_job = ["go1_projects.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"go1_projects.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
override_doctype_dashboards = {
	"Project": "go1_projects.project.get_dashboard_data"
}

