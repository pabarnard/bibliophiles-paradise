from flask_app import app
from flask import flash
import re
from datetime import date
from dateutil.relativedelta import relativedelta

email_regex = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.bookshelf = data["bookshelf"]
        self.reviews = data["reviews"]
        self.thoughts = data["thoughts"]

    @classmethod
    def find_by_username(cls, data):
        pass

    @classmethod
    def register_new_user(cls, data):
        pass

    @staticmethod
    def validate_registration(form_data):
        print(form_data)
        all_valid = True
        if "username" not in form_data or form_data["username"] == "":
            flash("Please enter a username!","username")
            all_valid = False
        elif len(form_data["username"]) < 3:
            flash("Your username must be 3 or more characters!", "username")
            all_valid = False
        # To add: validation for unique username
        # elif check database

        # Test email validation with regex
        if not email_regex.match(form_data["email"]):
            flash("Your email is in an invalid format.", "email")
            all_valid = False
        # To add: check for unique email
        # elif check database

        # Check birthdate - must be 18 years or older, but first check if it's entered
        if "birthdate" not in form_data:
            flash("Please enter a birthdate.  You must be at least 18 to register.", "birthdate")
            all_valid = False
        else: 
            entered_date = date.fromisoformat(form_data["birthdate"]) 
            if entered_date + relativedelta(years=+18) > date.today():
                flash("You must be at least 18 to register.", "birthdate")
                all_valid = False
        # Check passwords: start and check if either one is blank or missing
        if "password" not in form_data or form_data["password"] == "":
            flash("Please enter a valid password that's 8 through 30 characters long, with at least one uppercase letter, one lowercase letter, one number and one symbol (except '_').", "password")
            all_valid = False
        elif "confirmed_password" not in form_data or form_data["confirmed_password"] == "": 
            flash("Please confirm your password!  It must be 8 through 30 characters long, with at least one uppercase letter, one lowercase letter, one number and one symbol (except '_').", "password")
            all_valid = False
        # Check for matching passwords
        elif form_data["password"] != form_data["confirmed_password"]:
            flash("Your passwords must match!  Passwords must be 8 through 30 characters long, with at least one uppercase letter, one lowercase letter, one number and one symbol (except '_').", "password")
            all_valid = False
        # Now both passwords are filled in and matching, so check and see if it's in the proper format
        else:
            # Check for numbers, lower and upper case letters, and symbols
            has_upper, has_lower, has_digit, has_special = False, False, False, False
            for cur_char in form_data["password"]:
                # cur_char = ""
                if cur_char.isupper():
                    # print(cur_char + " is upper")
                    has_upper = True
                elif cur_char.islower():
                    # print(cur_char + " is lower")
                    has_lower = True
                elif cur_char.isdigit():
                    # print(cur_char + " is digit")
                    has_digit = True
                elif re.match(r"^\W$", cur_char): # Special character that's not the underscore _
                    print(cur_char + " is special")
                    has_special = True
            # print(has_upper, has_lower, has_digit, has_special)
            if not has_upper or not has_lower or not has_digit or not has_special or \
                len(form_data["password"]) < 8 or len(form_data["password"]) > 30:
                flash("Your password must be 8 through 30 characters long, with at least one uppercase letter, one lowercase letter, one number and one symbol (except '_').", "password")
                all_valid = False
        return all_valid
    
    @staticmethod
    def validate_login(form_data):
        pass
