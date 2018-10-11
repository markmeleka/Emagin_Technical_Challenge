from contextlib import contextmanager

import graphene
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from models import db_session, Department as DepartmentModel, \
	Employee as EmployeeModel
from objects import EmployeeObject


@contextmanager
def make_session_scope(Session=db_session):
	session = Session()
	session.expire_on_commit = False
	try:
		yield session
	except SQLAlchemyError:
		session.rollback()
		raise
	finally:
		session.close()


class DepartmentInput(graphene.InputObjectType):
	name = graphene.String(required=True)


class EmployeeInput(graphene.InputObjectType):
	name = graphene.String(required=True)
	salary = graphene.Int(required=True)
	department = graphene.InputField(DepartmentInput, required=True)


class CreateEmployee(graphene.Mutation):
	class Arguments:
		employee_data = EmployeeInput(required=True)

	ok = graphene.Boolean()
	employee = graphene.Field(EmployeeObject)

	@staticmethod
	def mutate(self, args, employee_data=None):
		with make_session_scope() as sess:
			department = sess.query(DepartmentModel) \
				.filter(func.lower(DepartmentModel.name) == \
					func.lower(employee_data.department.name)) \
				.first()
			# If the department doesn't exist, create it.
			if not department:
				department = DepartmentModel(name=employee_data.department.name)
			# TODO: Capitalize department name
			# TODO: Sanitize inputs?
			employee = EmployeeModel(
				name=employee_data.name,
				salary=employee_data.salary,
				department=department
				)
			sess.add(employee)
			sess.commit()
			return CreateEmployee(employee=employee, ok=True)


class DeleteEmployee(graphene.Mutation):
	class Arguments:
		id = graphene.ID(required=True)

	ok = graphene.Boolean()

	def mutate(self, info, **args):
		with make_session_scope() as sess:
			if args.get('id'):
				sess.query(EmployeeModel) \
					.filter(EmployeeModel.id == args.get('id')) \
					.delete(synchronize_session=False)
				sess.commit()
				return DeleteEmployee(ok=True)
			else:
				return DeleteEmployee(ok=False)

