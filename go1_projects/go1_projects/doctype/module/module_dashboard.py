from frappe import _

def get_data():
	return {
		'fieldname': 'module',
		# 'non_standard_fieldnames': {
		# 	'Journal Entry': 'reference_name',
		# 	'Salary Slip': 'employee'
		# 	},
		'transactions': [
			{
				'label': _('Screen'),
				'items': ['Screen']
			},

			{
				'label': _('Bugs'),
				'items': ['Bug Sheet']
			},
			{
				'label': _('Test Case'),
				'items': ['Test Case']
			}
			# {
			# 	'label': _('Employee'),
			# 	'items': ['Salary Slip']
			# }			
		]
	}