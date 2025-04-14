from flask_app import app
from flask_app.models import book
from flask_app.services import google_books_api
from flask import request, flash, render_template, session, redirect, url_for, get_flashed_messages

@app.route("/books")
def all_books():
    if "user_id" not in session:
        return redirect(url_for("registration"))
    all_books = book.Book.get_all()
    return render_template("all_books.html", all_books = all_books)

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
    if "user_id" not in session:
        return redirect(url_for("registration"))
    is_valid = book.Book.validate_isbn(request.form) # Validate ISBN
    # Save form data when page reloads
    session["isbn"] = request.form.get("isbn", "")
    if not is_valid:
        return redirect(url_for("search_page"))
    # Fetch results and keep track of which ones have been saved in the database and saved in user's shelf
    google_book_ids_in_db = book.Book.get_all_ids()
    shelf_google_volume_ids = book.Book.get_google_volume_ids_in_shelf({"user_id": session["user_id"]})
    book_results = google_books_api.get_books_by_isbn(request.form, google_book_ids_in_db, shelf_google_volume_ids)
    # NOTE: In the future, add logic for if there's an error with the API
    session["book_results"] = book_results
    return redirect(url_for("search_page"))

@app.route("/search-by-title-and-author", methods=["POST"])
def search_by_title_and_author():
    if "user_id" not in session:
        return redirect(url_for("registration"))
    is_valid = book.Book.validate_title_and_author(request.form)
    # Save form data when page reloads
    session["author"] = request.form.get("author", "")
    session["title"] = request.form.get("title", "")
    if not is_valid:
        return redirect(url_for("search_page"))
    # Fetch results and keep track of which ones have been saved in the database and saved in user's shelf
    google_book_ids_in_db = book.Book.get_all_ids()
    shelf_google_volume_ids = book.Book.get_google_volume_ids_in_shelf({"user_id": session["user_id"]})
    book_results = google_books_api.get_books_by_title_and_author(request.form, google_book_ids_in_db, shelf_google_volume_ids)
    # NOTE: In the future, add logic for if there's an error with the API
    session["book_results"] = book_results
    return redirect(url_for("search_page"))

@app.route("/add-book-to-database-and-shelf", methods=["POST"])
def add_book_to_database():
    if "user_id" not in session:
        return redirect(url_for("registration"))
    volume_id = request.form["google_volume_id"]
    # NOTE: Reserved for handling errors from API, and if there's an invalid or no Google Volume ID
    # if "book_results" not in session or volume_id not in session["book_results"]:
    #     pass
    book_info = session["book_results"][volume_id]
    book_info["google_volume_id"] = volume_id # Save volume ID from Google in data dictionary before saving in the database
    book_info["user_id"] = session["user_id"] # For saving the new book to the user's bookshelf
    # FUTURE: Try to find a way to consolidate these three separate database calls into one connection
    book.Book.create(book_info) # Save book in database
    new_book_obj = book.Book.get_by_google_id({"google_volume_id": book_info["google_volume_id"]}) # Now fetch new book in database
    book.Book.add_to_shelf({"book_id": new_book_obj.id, "user_id": session["user_id"]}) # Save new book in user's bookshelf
    return redirect(url_for("all_books")) # NOTE: This is a TEMPORARY route