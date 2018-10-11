import graphene
from graphene.test import Client

from schema import schema


def test_create_employee():
	client = Client(schema)
	query = '''
		mutation {
		  createEmployee(employeeData: {name: "John Doe", salary: 100, department: {name: "Engineering"} }) {
		    employee {
		      name
		      salary
		      department {
		        name
		      }
		    }
		  }
		}
	'''    
	
	executed = client.execute(query)

	assert executed == {
	  "data": {
	    "createEmployee": {
	      "employee": {
	        "name": "John Doe",
	        "salary": 100,
	        "department": {
	          "name": "Engineering"
	        }
	      }
	    }
	  }
	}


if __name__ == '__main__':
	test_create_employee()