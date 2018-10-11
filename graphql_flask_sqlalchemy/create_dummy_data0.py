from models import engine, db_session, Base, Department as DepartmentModel, Employee as EmployeeModel

# DEPRECATED IN FAVOUR OF create_dummy_data.py

# This is roughly the direction suggested in the Graphene-Python tutorial
# http://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/


def main():
	# Drop everything for a clean slate.
	Base.metadata.drop_all(engine)

	Base.metadata.create_all(bind=engine)


	# Fill the tables with some data
	engineering = DepartmentModel(name='Engineering')
	db_session.add(engineering)
	hr = DepartmentModel(name='Human Resources')
	db_session.add(hr)

	peter = EmployeeModel(
		name='Peter', 
		salary = 90000, 
		department=engineering)
	db_session.add(peter)

	roy = EmployeeModel(
		name='Roy', 
		salary = 120000, 
		department=engineering)
	db_session.add(roy)

	tracy = EmployeeModel(
		name='Tracy', 
		salary = 75000, 
		department=hr)
	db_session.add(tracy)

	db_session.commit()


if __name__ == '__main__':
	main()