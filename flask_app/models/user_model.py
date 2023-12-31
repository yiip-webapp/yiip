from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import business_model

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    db = "mydb"

    def __init__( self, data_row ):
        self.id = data_row['id']
        self.first_name = data_row['first_name']
        self.last_name = data_row['last_name']
        self.email = data_row['email']
        self.password = data_row['password']
        self.birthday = data_row['birthday']
        self.created_at = data_row['created_at']
        self.updated_at = data_row['updated_at']
        self.my_businesses = []

##### CREATE
##### CREATE
##### CREATE
    @classmethod
    def save(cls, data_row):
        query = """
        INSERT INTO users (first_name, last_name, email, password, birthday)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s), %(birthday)s);
        """

        user_first_name = data_row['first_name']
        user_id = connectToMySQL(cls.db).query_db( query, data_row)
        print("The name is here:" + user_first_name)
        return user_id
    
### READ
### READ
### READ
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL( cls.db ).query_db(query,data)
        if len(results) < 1:
            return False
        print(results)
        return cls(results[0])
    
    @classmethod
    def get_one_user( cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL( cls.db ).query_db(query, data)
        if results:
            return cls(results[0])
        return False


### UPDATE
### UPDATE
### UPDATE
    @classmethod
    def edit_user(cls,data):
        query = """
                UPDATE users SET id = %(id)s, first_name = %(first_name)s, last_name = %(last_name)s, 
                email = %(email)s, password = %(password)s, birthday = %(birthday)s WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        return results


### DELETE
### DELETE
### DELETE
    @classmethod
    def delete_user(cls, data_row):
        query = """
                DELETE FROM users WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data_row)
        return results



    @staticmethod
    def validate_user(form):
        is_valid = True
        errors = {}
        if len(form['first_name']) < 2:
            is_valid = False
            errors["first_name"] = "Your first name must be two characters or more."
        if len(form['last_name']) < 2:
            is_valid = False
            errors["last_name"] ="Your last name must be two characters or more."
        if not EMAIL_REGEX.match(form['email']):
            is_valid = False
            errors["email"] ="Your email address must be in a valid format."

            # Check if the email is already used - Noah
        if len(form['password']) < 8:
            is_valid = False
            errors["password"] ="Your password must be eight characters or more."
        if not form['password'] == form['confirm_password']:
            is_valid = False
            errors["confirm_password"] ="Your passwords must match."
        if (form['birthday']) < 18:
                is_valid = False
                errors["birthday"] ="You must be 18 years old or older to join yiip."
        return (is_valid, errors)