# This file will handle the Google Books API calls and then the controller will render the data.
from flask_app import app
from flask_app.models import book
from flask_app.services import google_books_api
from flask import request, flash, render_template, session, redirect, url_for, get_flashed_messages

@app.route("/search")
def search_page():
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

@app.route("/search-by-isbn", methods=["POST"])
def search_by_isbn():
    print(request.form)
    is_valid = book.Book.validate_isbn(request.form) # Validate ISBN
    # Save form data when page reloads
    session["isbn"] = request.form.get("isbn", "")
    if not is_valid:
        return redirect(url_for("search_page"))
    book_results = google_books_api.get_books_by_isbn(request.form)
    # NOTE: In the future, add logic for if there's an error with the API
    session["book_results"] = book_results
    return redirect(url_for("search_page"))

@app.route("/search-by-title-and-author", methods=["POST"])
def search_by_title_and_author():
    is_valid = book.Book.validate_title_and_author(request.form)
    # Save form data when page reloads
    session["author"] = request.form.get("author", "")
    session["title"] = request.form.get("title", "")
    if not is_valid:
        return redirect(url_for("search_page"))
    book_results = google_books_api.get_books_by_title_and_author(request.form)
    # NOTE: In the future, add logic for if there's an error with the API
    session["book_results"] = book_results
    return redirect(url_for("search_page"))