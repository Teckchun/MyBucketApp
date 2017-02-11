# MyBucketApp
Database set up:
Database script located in folder MyBucketApp/sqlscript -> MyBucketList.sql
# Technology Usage
 #DBMS: Mysql  <br>
 #Backend: <br>
  WebServer framework: Flask <br>
  Language: Python 2.7 <br>
  #Frontend: <br>
HTML,CSS,Bootstrap,Bootswatch,jQuery,jQuery Template,Jinja2
# Deployment:
1. clone the project
2. cd to project folder
3. install some library:  <br>
<code>
  $ pip install requests <br>
  $ pip install flaskext.mysql <br>
</code>
4. open app.py and change database configuration
   app.config['MYSQL_DATABASE_HOST'] = 'localhost'
   app.config['MYSQL_DATABASE_PORT'] = 3306
   app.config['MYSQL_DATABASE_USER'] = 'your_db_username'
   app.config['MYSQL_DATABASE_PASSWORD'] = 'your_db_password'
   app.config['MYSQL_DATABASE_DB'] = 'your_databaseName'

# How to access
url: http://localhost:5000   (for index page)












