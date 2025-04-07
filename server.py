from flask_app import app
from flask_app.controllers import user_controller
from flask_app.services import google_books_api
from flask import session, redirect, url_for, render_template

@app.route("/dashboard") # TEMPORARY route - landing page - for testing registration, logging in and logging out
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("registration"))
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True,port=5001)