from flask import Flask
import app
from app.home import home_index

app = Flask(__name__)

@app.route('/')
def index():
    return home_index()

