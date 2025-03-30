from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("") # Will hold secret key, environment keys, passwords, etc. from .env file

app = Flask(__name__)
