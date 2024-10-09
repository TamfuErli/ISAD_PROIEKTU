from flask import Flask, render_template
from flask import request


def home_index():
    return render_template('home.html')


