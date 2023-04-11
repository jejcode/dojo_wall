from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import post,comment # import other models to create instances from here
from flask import flash # use flash to store validation messages

import re # import regex to validate email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # string to ensure valid email address
PASS_REGEX = re.compile(r'^(?!^[0-9]*$)(?!^[a-zA-Z]*$)^([a-zA-Z0-9!@#$%^&*()]{8,})$') # string to check password for letters and numbers

class User:
    DB = 'coding_dojo_wall_schema'
    def __init__(self, data) -> None: # columns in database match instance attributes
        print('making User instance...')
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = [] # each post by this user will be gathered here
        self.comments = [] # each comment instance will be stored here

    # CRUD
    # CREATE
    @classmethod
    def add_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s)"""
        return connectToMySQL(cls.DB).query_db(query, data) # returns row ID of new user
    # READ
    @classmethod
    def get_user_by_email(cls, data): # get db row from user email
        query = "SELECT * FROM users where email = %(email)s"
        results = connectToMySQL(cls.DB).query_db(query, data) # results in a list of one
        if len(results) < 1:
            return 0
        return cls(results[0]) # create an instance from db row and return it
    @classmethod
    def get_user_by_id(cls, data): # get db row from users table by this id
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    # static methods for user form validations
    @staticmethod
    def validate_registration(data):
        print('validating...')
        is_valid = True
        if len(data['fname']) < 2:
            flash('First name must have at least 2 characters.', 'registration')
            is_valid = False
        if len(data['lname']) < 2:
            flash('Last name must have at least 2 characters.', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash('Invalid email address!', 'registration')
            is_valid = False
        if User.get_user_by_email({'email': data['email']}):
            flash('Email is already in use.', 'registration')
            is_valid = False
        if not PASS_REGEX.match(data['password']):
            flash('Password must contain at least one letter, one number, and be at least 8 characters long.', 'registration')
            is_valid = False
        if data['confirm'] != data['password']:
            flash('Password does not match confirm password', 'registration')
            is_valid = False
        print('validation result:', is_valid)
        return is_valid