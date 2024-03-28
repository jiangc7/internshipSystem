###init project structure 
###all teammate should read this before you start to code. 

#the app.py is split into many  routes and organized by Blueprint.

###Route rules:
UserRoute for instance, the name of the route is declare at the top of the file.
userRoute = Blueprint('userRoute', __name__)

and all the route inside of the userRoute is started with @userRoute.route followed with your route url. '/mentor/getAll'

and register userRoute to app.py which is our main route.

from UserRoute import userRoute
app = Flask(__name__)
app.register_blueprint(userRoute)

then front-end should be ok to call the route.
***

###Sessions variables:
all logged in user's id, name and role is store into sessions

front-end can call the session by     
{{session['name']   }} or 
{{session['user_id']   }} or 
{{session['role']   }} or 
{{session['email']   }}  

***
###Queries:

All queries are split by its functionalities,
such as user related queries is stored into userQueries.py

and import into UserRoute.py
by 'from queries import UsersQueries'

Almost all the queries.py have already wrote
select, insert, update, delete statements
which can provide a quick start on your task

but only select statement have a route. 

if you want to add a query function 
you can simply just
first write a correct sql statement;
second call a function provided by db.py


YourSQL= 'xxxxxxxxxx xxxx    xxxxxxxx'

such as db.DBOperatorInsertedId(YouSQL) is for 
add a row and return the insert data id
you can assign the db.DBOperatorInsertedId(YouSQL) into a variable to get an return id;
returnID = db.DBOperatorInsertedId(YouSQL)

db.DBOperator(YourSQL) returns a list of dictionary the key is the column name ,the value is the selected value

such as :

[
{'user_id': 32, 'first_name': 'newUser', 'last_name': 'lasnamennnnki,ol', 'password': 'facb8af02d66638c0590db2065231a08', 'email': 'liuwerwe32432@qwe.com123123', 'role': 0},
{'user_id': 33, 'first_name': 'newUser2', 'last_name': 'lasnamennnnki,ol2', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'email': 'aStudent@sss.com2', 'role': 2}
]

so front-end can easily visit the selected element
    {% for user in users %}
         {{ user['email'] }}
    {% endfor %}


###if you have any questions please feel free contact with me(Yang Liu)



 


  