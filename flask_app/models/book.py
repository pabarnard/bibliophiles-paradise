from flask_app import db_name
from flask import flash
from flask_app.config.mysql_connection import connect_to_db
import re

class Book:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.google_volume_id = data.get("google_volume_id")
        self.title = data.get("title")
        self.authors = data.get("authors")
        self.publication_date = data.get("publication_date")
        self.page_count = data.get("page_count")
        self.thumbnail = data.get("thumbnail")
        self.isbn13 = data.get("isbn13")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")
        self.thoughts = data.get("thoughts")
        self.reviews = data.get("reviews")
        self.readers = data.get("readers") # Users who added this book to their shelves
    
    """
    Source: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html
    Regular Expressions Cookbook, 2nd Edition by Jan Goyvaerts, Steven Levithan

    This method validates the ISBN of a book.  This works regardless of including spaces, dashes, "ISBN-", etc. in the right spots.
    """
    @staticmethod
    def validate_isbn(form_data):
        is_valid = True
        # Missing input
        if "isbn" not in form_data or form_data["isbn"] == "":
            flash("Please include a 10- or 13-digit ISBN.","isbn")
            return False
        isbn_input = form_data["isbn"]
        # Checks for ISBN-10 or ISBN-13 format
        regex = re.compile("^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$")
        if regex.search(isbn_input):
            # Remove non ISBN digits, then split into a list
            chars = list(re.sub("[- ]|^ISBN(?:-1[03])?:?", "", isbn_input))
            # Remove the final ISBN digit from `chars`, and assign it to `last`
            last = chars.pop()
            if len(chars) == 9:
                # Compute the ISBN-10 check digit
                val = sum((x + 2) * int(y) for x,y in enumerate(reversed(chars)))
                check = 11 - (val % 11)
                if check == 10:
                    check = "X"
                elif check == 11:
                    check = "0"
            else:
                # Compute the ISBN-13 check digit
                val = sum((x % 2 * 2 + 1) * int(y) for x,y in enumerate(chars))
                check = 10 - (val % 10)
                if check == 10:
                    check = "0"
            if str(check) != last:
                print("Invalid sequence for ISBN")
                flash("This is an improper 10- or 13-digit ISBN.","isbn")
                is_valid = False
        else:
            print("REGEX failure")
            flash("This is an improper 10- or 13-digit ISBN.","isbn")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_title_and_author(form_data):
        # NOTE: In the future, make it so that one can search EITHER title or author and not need both.
        is_valid = True
        if "author" not in form_data or form_data["author"] == "":
            flash("Please type the author's name.","author")
            is_valid = False
        if "title" not in form_data or form_data["title"] == "":
            flash("Please type the title of the book.","title")
            is_valid = False
        return is_valid