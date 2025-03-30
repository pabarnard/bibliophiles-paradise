from flask_app import app

@app.route("/")
def test_route():
    return "Hello there!"

if __name__=="__main__":
    app.run(debug=True,port=5001)