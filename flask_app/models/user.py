import re	# the regex module
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import boardgame, comment, mechanic
from datetime import date, datetime

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$')
LOCATION_REGEX = re.compile(r'^\d{5}$')
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.about = data['about']
        self.location = data['location']
        self.birthday = data['birthday']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def delete( cls, data ):
        query = "DELETE FROM users where ID = %(id)s;"
        return connectToMySQL('meeple').query_db(query, data)

    # class method to save our user to the database
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO users ( first_name , last_name, email, location, birthday, password, created_at, updated_at ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(location)s, %(birthday)s, %(password)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def add_about ( cls, data ):
        query = "UPDATE users SET about = %(about)s, updated_at = NOW() WHERE id = %(id)s; "
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def update_user (cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, about = %(about)s, location = %(location)s, birthday = %(birthday)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def change_password (cls, data):
        query = "UPDATE users SET password = %(password)s WHERE id = %(id)s;"
        return connectToMySQL('meeple').query_db(query, data)

    @staticmethod
    def validate( user ):
        is_valid = True

        # test whether the email already exists in the database
        query = "SELECT email FROM users"
        results = connectToMySQL('meeple').query_db(query)
        for one_user in results:
            if user['email'] == str(one_user['email']):
                flash("Email address already exists, please choose another one.")
                print("already exists")
                is_valid = False

        if(not user['first_name'] or not user['last_name'] or not user['location'] or not user['birthday'] or not user['email'] or not user['password']):
            flash("All fields are required.")
            is_valid = False

        if len(user['first_name']) < 3 or len(user['last_name']) < 2:
            flash("First and last name must be at least 2 characters.")
            is_valid = False

        if user['password'] != user['password2']:
            flash("Password fields do not match.")
            is_valid = False

        # test whether the email matches the correct pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address! Please try again with a valid email address.")
            is_valid = False

        # test whether the password matches the pattern
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Invalid password, it must be at least 8 characters long and contain at least one capital letter and one number")
            is_valid = False
        
        if not LOCATION_REGEX.match(user['location']):
            flash("Zip code must be 5 digits")
            is_valid = False

        today = date.today()
        dt = datetime.strptime(user['birthday'], '%Y-%m-%d')
        age = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))
        if age < 13:
            flash("You must be at least 13 years old to register.")
            is_valid = False

        return is_valid

    @staticmethod
    def validate_edit( user ):
        is_valid = True

        if(not user['first_name'] or not user['last_name'] or not user['location'] or not user['birthday']):
            flash("All fields are required.")
            is_valid = False

        if len(user['first_name']) < 3 or len(user['last_name']) < 2:
            flash("First and last name must be at least 2 characters.")
            is_valid = False
        
        if not LOCATION_REGEX.match(user['location']):
            flash("Zip code must be 5 digits")
            is_valid = False

        today = date.today()
        dt = datetime.strptime(user['birthday'], '%Y-%m-%d')
        age = today.year - dt.year - ((today.month, today.day) < (dt.month, dt.day))
        if age < 13:
            flash("You must be at least 13 years old to register.")
            is_valid = False

        return is_valid

    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('meeple').query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for one_user in results:
            users.append( cls(one_user) )
        return users

    @classmethod
    def get_id_by_email(cls, data):
        query = "SELECT id FROM users WHERE email = %(email)s;"
        results = connectToMySQL('meeple').query_db(query)
        if len(results) < 1:
            return False
        return cls(results[0])
        
    @classmethod
    def get_info_from_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('meeple').query_db(query, data)
        name = cls(results[0])
        return name

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('meeple').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_name_from_id(cls, data):
        query = "SELECT first_name FROM users WHERE id = %(id)s;"  
        results = connectToMySQL('meeple').query_db(query, data)
        return results

    @classmethod
    def add_friend(cls, data):
        query = "INSERT INTO friends (user_id, friend_id) SELECT %(user_id)s, %(friend_id)s WHERE NOT EXISTS (SELECT user_id, friend_id FROM friends WHERE user_id = %(user_id)s and friend_id = %(friend_id)s);"
        return connectToMySQL('meeple').query_db(query, data)

    @classmethod
    def get_friend_info(cls, data):
        query = "SELECT * FROM users JOIN friends ON friends.friend_id = users.id WHERE friends.user_id = %(id)s;"
        results = connectToMySQL('meeple').query_db(query, data)
        return results