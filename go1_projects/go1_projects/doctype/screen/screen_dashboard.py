from frappe import _

def get_data():
	return {
		'fieldname': 'screen',
		# 'non_standard_fieldnames': {
		# 	'Journal Entry': 'reference_name',
		# 	'Salary Slip': 'employee'
		# 	},
		'transactions': [
			{
				'label': _('Functionality'),
				'items': ['Screen Functionality']
			},

			{
				'label': _('Bugs'),
				'items': ['Bug Sheet']
			},
			{
				'label': _('Test Cases'),
				'items': ['Test Case']
			}
		]
	}