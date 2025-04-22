from flask_app import app
from flask_app.models import user
from flask_app.services import google_books_api
from flask import request, render_template, session, redirect, url_for, get_flashed_messages

@app.route("/my-library")
def my_library():
    if "user_id" not in session:
        return redirect(url_for("registration"))
    user_with_books = user.User.get_user_with_books({"id": session["user_id"]})
    return render_template("my_library.html", this_user = user_with_books)