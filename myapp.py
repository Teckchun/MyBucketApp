from peewee import *
from flask import (Flask,render_template,request,
    json)
from werkzeug import generate_password_hash, check_password_hash
mysql_db = MySQLDatabase('BucketList',user='root',password='root')
# ('database_name', user='www-data', charset='utf8mb4')
class User(Model):
    """docstring for ClassName"""
    class Meta:
        database = mysql_db
        user_name = CharField(max_length=45, unique=True)
        user_username = CharField(max_length=45)
        user_password = CharField(max_length=45)
    #create user
    def insertUser():
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        User.create(user_name=_name,
                user_username = _email,
                user_password = _password
                )
if __name__ == '__main__':
        mysql_db.connect()
        insertUser()









        