from models import engine, db_session, Base, Department as DepartmentModel, Employee as EmployeeModel

# Drop everything for a clean slate.
Base.metadata.drop_all(engine)

Base.metadata.create_all(bind=engine)


#Fill the tables with some data
engineering = DepartmentModel(name='Engineering')
db_session.add(engineering)
hr = DepartmentModel(name='Human Resources')
db_session.add(hr)

peter = EmployeeModel(name='Peter', salary = 90000, department=engineering)
db_session.add(peter)
roy = EmployeeModel(name='Roy', salary = 120000, department=engineering)
db_session.add(roy)
tracy = EmployeeModel(name='Tracy', salary = 75000, department=hr)
db_session.add(tracy)

db_session.commit()
