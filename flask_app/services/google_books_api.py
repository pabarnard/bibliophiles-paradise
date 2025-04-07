# This file will handle the Google Books API calls and then the controller will render the data.
from flask_app import app
from flask import request, flash, render_template, session, redirect, url_for, get_flashed_messages
import requests, os

# NOTE: This will be reorganized in terms of routing and logic soon!

@app.route("/search-by-isbn", methods=["POST"])
def search_by_isbn():
    # NOTE: Will move validation to Book model soon
    is_valid = True
    if "isbn" not in request.form or request.form["isbn"] == "":
        flash("Please include a 10- or 13-digit ISBN.","isbn")
        is_valid = False
    elif len(request.form["isbn"]) not in [10, 13]: # will remove in a bit
        flash("Please type an ISBN that's only 10 or 13 digits.","isbn")
        is_valid = False
    # elif check for valid number
    
    # Save form data when page reloads
    session["isbn"] = request.form["isbn"]
    if not is_valid:
        return redirect("/search")
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params={
        "api_key": os.getenv("GOOGLE_API_KEY"), 
        "q": "isbn:"+request.form["isbn"],
        "langRestrict": "en"
        })
    json_data = r.json()
    book_results = process_data(json_data)
    session["book_results"] = book_results
    return redirect("/search")

@app.route("/search-by-title-and-author", methods=["POST"])
def search_test():
    # NOTE: Will move validation to Book model soon
    print(request.form)
    is_valid = True
    if "author" not in request.form or request.form["author"] == "":
        print("VALIDATION AUTHOR ERROR")
        flash("Please type the author's name.","author")
        is_valid = False
    if "title" not in request.form or request.form["title"] == "":
        print("VALIDATION TITLE ERROR")
        flash("Please type the title of the book.","title")
        is_valid = False
    # Save form data when page reloads
    session["author"] = request.form["author"]
    session["title"] = request.form["title"]
    if not is_valid:
        return redirect("/search")
    # API is WORKING
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params={
        "api_key": os.getenv("GOOGLE_API_KEY"), 
        "q": "intitle:"+request.form["title"]+"+"+"inauthor:"+request.form["author"],
        "langRestrict": "en"
        })
    json_data = r.json()
    book_results = process_data(json_data)
    session["book_results"] = book_results
    return redirect("/search")

@app.route("/search") # NOTE: Will be moved to another controller
def search():
    if "user_id" not in session:
        return redirect(url_for("registration"))
    form_data = {}
    form_data["author"] = session.get("author", "")
    form_data["title"] = session.get("title", "")
    form_data["isbn"] = session.get("isbn", "")
    book_results = session.get("book_results", [])
    error_msgs = get_flashed_messages(with_categories=True)
    error_data = {
        "author": "",
        "title": "",
        "isbn": ""
    }
    for key, msg in error_msgs:
        error_data[key] = msg    
    return render_template("search_page.html", error_data = error_data, book_results = book_results, form_data = form_data)

# Helper function to process raw JSON data and convert it to a form that can be saved in the database
def process_data(raw_json):
    all_books = []
    for book in raw_json['items']:
        book_info = book['volumeInfo']
        print(book_info)
        clean_book_dict = {}
        clean_book_dict["google_volume_id"] = book['id'] if 'id' in book else ""
        clean_book_dict["title"] = book_info['title'] if 'title' in book_info else ""
        
        if "authors" in book_info:
            all_authors = ""
            for author in book_info['authors']:
                if all_authors != "":
                    all_authors += ", "
                all_authors += author
            clean_book_dict["authors"] = all_authors
        else:
            clean_book_dict["authors"] = ""
        clean_book_dict["publication_date"] = book_info['publicationDate'] if 'publicationDate' in book_info else ""
        clean_book_dict["page_count"] = book_info['pageCount'] if 'pageCount' in book_info else ""
        if "imageLinks" in book_info:
            clean_book_dict["thumbnail"] = book_info["imageLinks"]["thumbnail"] if "thumbnail" in book_info["imageLinks"] else ""
        else:
            clean_book_dict["thumbnail"] = ""
        if "industryIdentifiers" in book_info:
            for identifier in book_info["industryIdentifiers"]:
                if identifier["type"] == "ISBN_13":
                    clean_book_dict["isbn13"] = identifier["identifier"]
                    break
                elif identifier["type"] == "ISBN_10":
                    clean_book_dict["isbn13"] = "978"+identifier["identifier"] # Convert from ISBN10 to ISBN13
            if "isbn13" not in clean_book_dict:
                clean_book_dict["isbn13"] = ""
        else:
            clean_book_dict["isbn13"] = ""
        all_books.append(clean_book_dict)
    return all_books