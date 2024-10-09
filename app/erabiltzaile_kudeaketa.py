from flask import Flask, render_template
from flask import request

def erabiltzaile_kudeaketa():
    return render_template('erabiltzaile_kudeaketa.html')