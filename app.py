from flask import (Flask,render_template,request,
	json,redirect)
#from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
# Restricted unauthorized access
from flask import session

app = Flask(__name__)
app.secret_key = 'appSecret'

mysql = MySQL()
# MySQL configurations


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
mysql.init_app(app)


@app.route('/')
@app.route('/main')
def index():
    if session.get('user'):
	    return render_template('userHome.html',userName=session['username'])
    else:
        return render_template('index.html')

#sign up view
@app.route('/showSignUp')
def ShowSignUp():
    if session.get('user'):
        return redirect('/userHome')
        # return render_template('userHome.html',userName=session['username'])
    else:
        return render_template('signup.html')

#sign in view
@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

# userHome
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html',userName=session['username'],displayName=session['displayName'])
    else:
        return render_template('error.html',error="Unauthorized Access")
    return render_template('userHome.html')    


#validate Login
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        #get user name and password from input fields
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
 
 
        # connect to mysql
 
        con = mysql.connect()
        # create cursor to call procedure
        cursor = con.cursor()
        #calling validate login store procedure to validate username
        cursor.callproc('sp_validateLogin',(_username,))
        # Get the fetched records from the cursor

        data = cursor.fetchall()
        if len(data) > 0:
            print(data)
            print(_password)
            '''
            check_password_hash to check if the returned hash password matches
            the password entered by the user.
            '''
            print("hey")
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                session['displayName'] = data[0][1]
                print(data[0][1])
                session['username'] = _username
                # print("data [0][0]..{}".format(data[0][0]))
                print("success")
                return redirect('/userHome')
            else:
                print("wrong pw ")
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            print("error")
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()




  

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
            print(_hashed_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
    else:
    	return json.dumps({'html':'<span>Please fill out required fields!</span>'})


#logout
@app.route('/logout')
def logout():
    session.pop('user',None);
    return redirect('/')
#showList
@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')

#call addWish store procedure
@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish',(_title,_description,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                print("add successful!")
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()
#getAll wish
@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
 
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
 
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)
 
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))


#get wish by Id
@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetWishById',(_id,_user))
            result = cursor.fetchall()

            # array of wish
            wish = []
            wish.append({
                'Id':result[0][0],
                'Title':result[0][1],
                'Description':result[0][2]
                })
            return json.dumps(wish)
        else:
            return render_template('error.html',error="Unauthrized access")
    except Exception as e:
        return render_template('error.html',error=str(e))

#update wishlist detail
@app.route('/updateWish', methods=['POST'])
def updateWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _wish_id = request.form['id']
 
 
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateWish',(_title,_description,_wish_id,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
        conn.close()
# delete wishlist
@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteWish',(_id,_user))
            result = cursor.fetchall()
 
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()


if __name__=='__main__':
	app.run(debug=True)

