from flask import (Flask,render_template,request,
	json)
#from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
app = Flask(__name__)

#configure mysql
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'BucketList'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)






@app.route('/')
@app.route('/main')
def index():
	return render_template('index.html')

#sign up view
@app.route('/showSignUp')
def ShowSignUp():
	return render_template('signup.html')

@app.route('/SignUp',methods=['POST'])
def SignUp():
	# create user 
    # getting post request from view
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']


    #validate value 
    if _name and _email and _password:
    	
    	  # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
    else:
    	return json.dumps({'html':'<span>Please fill out required fields!</span>'})




if __name__=='__main__':
	app.run(debug=True)

