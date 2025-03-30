from flask_app import app

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.bookshelf = data["bookshelf"]
        self.reviews = data["reviews"]
        self.thoughts = data["thoughts"]