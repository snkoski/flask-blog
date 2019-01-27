from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime


# @before_request decorator exucutes this function right before the view functions
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
# route decorator from Flask-Login requireing a user to be logged in to access the route
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'title': 'PORTLAND TIMES',
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'title': 'Movie Reviews',
            'body': 'The Avengers movie was so cool!'
        }
    ]
    # render index template and pass user variable in route to user variable in index.html
    return render_template('index.html', title='Home Page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # current_user variable comes from Flask-Login, redirect to index page if a user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # choose which form this route will render
    form = LoginForm()
    # if form is valid find user in database with username from form and set to assign to user variable
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If username is not found in database or password doesn't match flash message and redirect back to login form
        if user is None or not user.check_password(form.password.data):
            flash('Invalide username or password')
            return redirect(url_for('login'))
        # login_user() comes from Flask-Login, register the user as logged in and set to current_user variable
        login_user(user, remember=form.remember_me.data)
        # redirect a user back to the page they were trying to access after logging in
        # request variable contains all the unformation that the client sent with the request
        next_page = request.args.get('next')
        # redirect to index if there was no next argument in the request
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# use logout_user() from Flask-Login
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'title': 'Test Title One', 'body': 'Test post body #1'},
        {'author': user, 'title': 'Test Title 2', 'body': 'Test post body #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
