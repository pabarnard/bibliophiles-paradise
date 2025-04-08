from flask import Flask
from dotenv import load_dotenv
import os
from flask_bcrypt import Bcrypt
load_dotenv() # Load all env variables into the application; they don't need to be loaded again elsewhere

app = Flask(__name__)
bcrypt = Bcrypt(app) # For securing our passwords
app.secret_key = os.getenv("SECRET_KEY") # For session
db_name = "bibliophile_schema" # For our database