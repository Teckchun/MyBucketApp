from peewee import *
from flask import (Flask,render_template,request,
    json)
from werkzeug import generate_password_hash, check_password_hash

database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    class Meta:
        order_by = ('username',)
class Relationship(BaseModel):
    from_user = ForiegnKeyField(User,related_name='relationships')
    to_user = ForiegnKeyField(User,related_name='related_to')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('from_user', 'to_user'), True),
        )

class Message(BaseModel):
    user = ForeignKeyField(User)
    content = TextField()
    pub_date = DateTimeField()

    class Meta:
        order_by = ('-pub_date',)

def create_tables():
    database.connect()
    database.create_tables([User, Relationship, Message])









if __name__ == '__main__':
        mysql_db.connect()
        insertUser()









        