from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv() # Load all env variables into the application; they don't need to be loaded again elsewhere

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") # For session