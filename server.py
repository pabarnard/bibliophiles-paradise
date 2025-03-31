from flask_app import app
import requests
import os

@app.route("/")
def test_route():
    return "Hello there!"

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

if __name__=="__main__":
    app.run(debug=True,port=5001)