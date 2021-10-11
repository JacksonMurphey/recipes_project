from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt 
from recipes_app import app
from recipes_app.models import recipe 
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile('^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')


class User:
    db_name = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one_user(cls, data):
        query = 'SELECT * FROM users WHERE users.id = %(id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results: 
            return False
        else:
            return cls(results[0])

    @classmethod
    def get_one_by_email(cls, data):
        query = 'SELECT * FROM users WHERE users.email = %(email)s'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results: 
            return False
        else:
            return cls(results[0])

    @classmethod 
    def get_user_recipes(cls, data):
        query ='SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        user = cls(results[0])

        if results[0]['recipes.id'] == None:
            return cls(results[0])
        else:
            for recipe_dict in results:
                recipe_data = {
                    'id' : recipe_dict['recipes.id'],
                    'name' : recipe_dict['name'],
                    'description' : recipe_dict['description'],
                    'instructions' : recipe_dict['instructions'],
                    'date_made' : recipe_dict['date_made'],
                    'under_thirty' : recipe_dict['under_thirty'],
                    'created_at' : recipe_dict['recipes.created_at'],
                    'updated_at' : recipe_dict['recipes.updated_at'],
                }
                user.recipes.append(recipe.Recipe(recipe_data))
        return user 


    @staticmethod
    def validate_register(data): 
        is_valid = True
        #Avoid being Sassy, unless its a sassy site. 
        #Confirming the new user email matches the email format. 
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email: Must contain @ and .', 'register')
            is_valid = False

        #Confirming the new user is using a unique email, one that isnt already registered to another user. 
        e_data = {'email': data['email']}
        user = User.get_one_by_email(e_data)
        if user:
            flash('Email already exists', 'register')
            is_valid = False

        if not data['first_name'].isalpha():
            flash('First Name Requires letters', 'register')
            is_valid = False
        if not data['last_name'].isalpha():
            flash('Last Name Requires letters', 'register')
            is_valid = False
        if len(data['first_name']) < 2:
            flash('First Name must be at least 2 characters', 'register')
            is_valid = False
        if len(data['last_name']) < 2: 
            flash('Last Name must be at least 2 characters', 'register')
            is_valid = False

        if not PASSWORD_REGEX.match(data['password']):
            flash('Password must be between 6-20 characters', 'register')
            flash('Password must include a number')
            flash('Password must include one upper and lower case character', 'register')
            flash('Password must include a special character', 'register')
            is_valid = False
        
        # Password confirmation validation
        if not data['password'] == data['confirm_password']:
            flash('Passwords Must Match', 'register')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True

        e_data = {'email': data['email']}
        user = User.get_one_by_email(e_data)
        if not user:
            flash('Invalid Email/Password', 'login')
            is_valid = False
        elif not bcrypt.check_password_hash(user.password, data['password']):
            flash('Invalid Email/Password', 'login')
            is_valid = False
        return is_valid

    # @staticmethod       #not sure the correct way to write this yet. 
    # def login_check(user_id):
    #     is_valid = True 

    #     data = {'id': user_id}
    #     user = User.get_one_user(data)
    #     if not user in session:
    #         flash('Must be logged in')
    #     return is_valid
