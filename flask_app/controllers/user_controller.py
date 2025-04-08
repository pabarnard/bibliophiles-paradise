from flask import request, render_template, redirect, url_for, session, get_flashed_messages
from flask_app import app
from flask_app.models import user

@app.route("/", methods=["GET","POST"])
def registration():
    if "user_id" in session:
        return redirect(url_for("dashboard")) # Temporary home page
    if request.method == "GET":      
        error_data = {
            "username": "",
            "email": "",
            "birthdate": "",
            "password": "",
            "confirmed_password": "",
        }
        # Grab error messages from validations, if applicable
        error_msgs = get_flashed_messages(with_categories=True)
        for key, msg in error_msgs:
            error_data[key] = error_data[key] + " " + msg if error_data[key] else error_data[key] + msg
        return render_template("registration.html", 
            error_data = error_data, 
            form_data = session.get("form_data", {}))
    # At this point, it's a POST request
    if not user.User.validate_registration(request.form):
        session["form_data"] = request.form
        return redirect(url_for("registration"))
    session.clear() # Remove form data from session
    # Add user to database here while saving the user in session, then redirect to dashboard
    new_id = user.User.register_new_user(request.form)
    if new_id != None:
        session["user_id"] = new_id
        return redirect(url_for("dashboard"))
    else: # This will be the result of an error with the back end (500-series error eventually)
        return redirect(url_for("registration"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard")) # Temporary home page
    if request.method == "GET":      
        error_data = {
            "username": "",
            "password": ""
        }
        # Grab error messages from validations, if applicable
        error_msgs = get_flashed_messages(with_categories=True)
        for key, msg in error_msgs:
            error_data[key] = error_data[key] + " " + msg if error_data[key] else error_data[key] + msg
        return render_template("login.html", 
            error_data = error_data, 
            form_data = session.get("form_data", {}))
    # At this point, it's a POST request
    if not user.User.validate_login(request.form):
        session["form_data"] = request.form
        return redirect(url_for("login"))
    session.clear() # Remove form data from session
    # Now save the found user's id in session and log them in
    found_id = user.User.find_by_username(request.form)[0]["id"]
    if found_id != None:
        session["user_id"] = found_id
        return redirect(url_for("dashboard"))
    else: # This will be the result of an error with the back end (500-series error eventually)
        return redirect(url_for("registration"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("registration"))