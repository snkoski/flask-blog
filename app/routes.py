from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Shawn'}
    return render_template('index.html', user=user)