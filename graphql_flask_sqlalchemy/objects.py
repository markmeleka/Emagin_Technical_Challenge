from math import ceil

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Department as DepartmentModel, Employee as EmployeeModel
from helper_functions import get_arguments


class DepartmentObject(SQLAlchemyObjectType):
	class Meta:
		model = DepartmentModel
		interfaces = (relay.Node,)
	

class DepartmentConnection(relay.Connection):
	class Meta:
		node = DepartmentObject


class EmployeeObject(SQLAlchemyObjectType):
	class Meta:
		model = EmployeeModel
		interfaces = (relay.Node,)


class EmployeeConnection(relay.Connection):
	total_count = graphene.Int(description=("The total number of employees in "
		"the database."))

	def resolve_total_count(self, info, **args):
		arguments = get_arguments(info)

		if 'first' in arguments.keys() and 'goToPage' in arguments.keys():
			offset = (int(arguments['first'])*int(arguments['goToPage']) 
				- int(arguments['first']))
			return len(self.iterable) + offset

		return len(self.iterable)

	num_pages = graphene.Int(description=("The number of pages in the "
		"database. Calculated as the ceiling of "
		"(total_num_pages/num_items_per_page)."))

	def resolve_num_pages(self, info, **args):
		arguments = get_arguments(info)
		
		if 'first' in arguments.keys():
			if 'goToPage' in arguments.keys():
				offset = (int(arguments['first'])*int(arguments['goToPage']) 
					- int(arguments['first']))
				return (ceil((len(self.iterable) + offset) 
					/ int(arguments['first'])))
			return ceil(len(self.iterable)/int(arguments['first']))
		elif 'last' in arguments.keys():
			return ceil(len(self.iterable)/int(arguments['last']))

	current_page = graphene.Int(description=("Current page, as requested by "
		"goToPage."))

	def resolve_current_page(self, info, **args):
		arguments = get_arguments(info)
		
		if 'first' in arguments.keys():
			if 'goToPage' in arguments.keys():
				return arguments['goToPage']
			return 1
		else:
			return


	class Meta:
		node = EmployeeObject