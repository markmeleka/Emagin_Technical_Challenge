import random as r
from re import sub

import graphene
from graphene.test import Client

from schema import schema
from models import Base, engine

# Seed for reproducibility
r.seed(123)

# Clean slate: drop everything then create from scratch.
Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)

# Names from: 
# https://github.com/joke2k/faker/blob/master/faker/providers/person/en_GB/__init__.py
first_names_male = [
	'David', 'Paul', 'Christopher', 'Thomas', 'John', 'Mark', 'James',
	'Stephen', 'Andrew', 'Jack', 'Michael', 'Daniel', 'Peter', 'Richard',
	'Matthew', 'Robert', 'Ryan', 'Joshua', 'Alan', 'Ian', 'Simon', 'Luke',
	'Samuel', 'Jordan', 'Anthony', 'Adam', 'Lee', 'Alexander', 'William',
	'Kevin', 'Darren', 'Benjamin', 'Philip', 'Gary', 'Joseph', 'Brian',
	'Steven', 'Liam', 'Keith', 'Martin', 'Jason', 'Jonathan', 'Jake',
	'Graham', 'Nicholas', 'Craig', 'George', 'Colin', 'Neil', 'Lewis',
	'Nigel', 'Oliver', 'Timothy', 'Stuart', 'Kenneth', 'Raymond', 'Jamie',
	]

first_names_female = [
	'Susan', 'Sarah', 'Rebecca', 'Linda', 'Julie', 'Claire', 'Laura',
	'Lauren', 'Christine', 'Karen', 'Nicola', 'Gemma', 'Jessica',
	'Margaret', 'Jacqueline', 'Emma', 'Charlotte', 'Janet', 'Deborah',
	'Lisa', 'Hannah', 'Patricia', 'Tracey', 'Joanne', 'Sophie', 'Carol',
	'Jane', 'Michelle', 'Victoria', 'Amy', 'Elizabeth', 'Helen', 'Samantha',
	'Emily', 'Mary', 'Diane', 'Rachel', 'Anne', 'Sharon', 'Ann', 'Tracy',
	'Amanda', 'Jennifer', 'Chloe', 'Angela', 'Louise', 'Katie', 'Lucy',
	'Barbara', 'Alison', 'Sandra', 'Caroline', 'Clare', 'Kelly', 'Bethany',
	]

first_names = first_names_male + first_names_female

departments = [
	'Engineering', 'Design', 'Product', 'Human Resources', 'Marketing', 
	'Sales', 'Management', 'Operations', 'Accounting', 'Finance'
	]


def create_employee(employee_name, salary, department_name):
	client = Client(schema)
	query = '''mutation {{
		  		createEmployee(employeeData: {{
		  			name: "{employee_name}", 
		  			salary: {salary}, 
		  			department: {{name: "{department_name}"}} 
	  	  		}}) 
	  	  		{{employee {{
			  		name,
			  		salary,
			  		department {{name}}
		  		}}}}
			}}'''
	
	# Remove tabs and line breaks for query to work through client.
	query = sub('\s+', '', query)

	query = query.format(
		employee_name=employee_name, 
		salary=salary, 
		department_name=department_name
		)
	
	executed = client.execute(query)


def main():
	for i in range(150):
		create_employee(
			employee_name=r.choice(first_names), 
			salary=str(int(r.gauss(100, 20))*1000), 
			department_name=r.choice(departments)
			)


if __name__ == '__main__':
	main()