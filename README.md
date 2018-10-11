## My submission for Emagin's technical challenge.

### Setup:

 * Clone the repository  
 	* `git clone https://github.com/markmeleka/Emagin_Technical_Challenge.git`  
 * Create virtualenv and install package dependencies in requirements.txt  
 	* `virtualenv env`  
 	* `source env/bin/activate`  
 	* `pip install -r requirements.txt`  
 * Create dummy data  
 	* In the virtualenv run `python create_dummy_data.py`  
 * Run the GraphQL app  
 	* `python app.py`  
 * The app should be running localhost:5000/graphql  

### Notes:

 * You can add an employee ("createEmployee") and list all existing employees ("allEmployees").  
 * You can list the employees page-by-page.  
 	* Pagination works using the "first" argument combined with the "goToPage" argument.  
 		* I didn't implement pagination via an offset.  
 	* Total number of pages can be seen with the "numPages" field.  
 		* Doesn't work with "after" argument.  
 	* Current page can be seen with the "currentPage" field.  
 		* Doesn't work with "after" argument.  
 	* Go to nth page with the "goToPage" argument.  
 		* Doesn't work with "after" argument.  
 	* I didn't implement the feature to sort employees department name and department salary in a paginated manner.  
 		* I need some help with this one.  
 		* But, I did implement sorting by variable name.  
 	* It's manually tested. There's probably a lot more edge cases I could have tried and more exception handling I could have written.   
 		* I started writing tests but stopped.  
 		* I was going to experiment with Snapshot tests but stopped.  