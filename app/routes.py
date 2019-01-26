from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user_in_route = {'username': 'Shawn'}
    # render index template and pass user variable in route to user variable in index.html
    return render_template('index.html', user_in_html=user_in_route)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # choose which form this route will render
    form = LoginForm()
    # if form is valid flash message and redirect to index page
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
