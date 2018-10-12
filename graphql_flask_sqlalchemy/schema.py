import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.sql import label

from mutations import CreateEmployee, DeleteEmployee
from objects import DepartmentConnection, EmployeeObject, EmployeeConnection
from helper_functions import get_arguments
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel


class Query(graphene.ObjectType):
	node = relay.Node.Field()

	all_employees = relay.ConnectionField(
		EmployeeConnection,
		# offset=graphene.Int(),
		go_to_page=graphene.Int(description=("Goes to the page specified. "
			"'first' argument must be provided.")),
		sort_by=graphene.String(description=("Sorts results by a given "
			"field. Use dot notation. ie. \"employee.name\""
			" or \"department.name\". Add \" desc\" for descending."
			" ie. \"employee.salary desc\". Sort by department salary"
			"with department_salary.")),
		description=("Provides a list of all employees. Allows for pagination "
			"and sorting. (Note: obfuscates IDs.)")
		)

	def resolve_all_employees(self, info, sort_by=None, **args):
		arguments = get_arguments(info)

		if sort_by in ['department_salary', 'department_salary desc']:
			# The method of sorting by department_salary queries 
			# the entire database instead of just using the specified 
			# variables in `info`. 
			# This defeats the purpose of using GraphQL. 
			# Find a better way.
			
			db = db_session()

			dpt_salaries = db.query(
				EmployeeModel.department_id, 
				label(
					'department_salary', 
					func.avg(EmployeeModel.salary))
				)

			dpt_salaries = (dpt_salaries
				.group_by(EmployeeModel.department_id)
				.subquery())

			qs = (db.query(EmployeeModel)
				.join(DepartmentModel)
				.join(
					dpt_salaries, 
					EmployeeModel.department_id ==
						dpt_salaries.c.department_id)
				.order_by(sort_by)
				.all())

		else:
			qs = (EmployeeObject.get_query(info)
				.join(DepartmentModel)
				.order_by(sort_by)
				.all())

		if 'first' in arguments.keys() and 'goToPage' in arguments.keys():
			offset = (int(arguments['first'])*int(arguments['goToPage']) 
				- int(arguments['first']))
			qs = qs[offset::]

		return qs

	find_employee = graphene.Field(
		EmployeeObject,
		id=graphene.Int(),
		name=graphene.String(),
		salary=graphene.Int(),
		description=("Input an ID, name, or salary. " 
			"Returns first employee match.")
		)

	def resolve_find_employee(self, context, **kwargs):
		query = EmployeeObject.get_query(context)
		query = query.filter_by(**kwargs)
		return query.first()

	all_employees_native = SQLAlchemyConnectionField(
		EmployeeConnection,  
		description=("Return all employees. Built-in pagination and sorting. "
			"No option to see total pages, current page, or go to a "
			"specific page (for these options, use allEmployees).")
		)
	
	all_departments_native = SQLAlchemyConnectionField(
		DepartmentConnection,
		description="Returns all departments. Built-in pagination and sorting."
		)


class Mutation(graphene.ObjectType):
	create_employee = CreateEmployee.Field(description=("Creates a new "
		"employee given name, salary, and department. If provided department "
		"not found, new department is created."))
	delete_employee = DeleteEmployee.Field(description=("Given an employee id,"
		" deletes an employee."))


schema = graphene.Schema(query=Query, mutation=Mutation)