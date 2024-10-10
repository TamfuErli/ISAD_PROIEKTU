from flask import render_template,Flask,url_for

app = Flask(__name__, static_url_path='', template_folder='../templates/')

@app.route('/')
def home():
    return render_template('home.html')