import graphene
from graphene.test import Client

from schema import schema

def test_create_employee(snapshot):
    client = Client(my_schema)
    # This will create a snapshot dir and a snapshot file
    # the first time the test is executed, with the response
    # of the execution.
    snapshot.assert_match(client.execute(    	
    	'''
		mutation {
	  		createEmployee(employeeData: {name: "John Doe", salary: 100}) {
		    	employee {
      				name,
		      		salary
		    	}
		  	}
		}
		'''
	))

if __name__ == '__main__':
	test_create_employee(snapshot)