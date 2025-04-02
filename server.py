from flask_app import app
from flask_app.controllers import user_controller
from flask import render_template, session, redirect, url_for
import requests, os

@app.route("/search")
def search_test():
    # API is WORKING
    r = requests.get("https://www.googleapis.com/books/v1/volumes", params={
        "api_key": os.getenv("GOOGLE_API_KEY"), 
        "q": "intitle:"+"Jurassic Park"+"+"+"inauthor:"+"Michael Crichton",
        "langRestrict": "en"
        })
    print(r.json())
    return "Hi!"

@app.route("/dashboard") # TEMPORARY route - landing page - for testing registration, logging in and logging out
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("registration"))
    return render_template("dashboard.html")

if __name__=="__main__":
    app.run(debug=True,port=5001)