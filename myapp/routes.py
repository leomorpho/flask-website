from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user,  \
    login_required
from werkzeug.urls import url_parse
from datetime import datetime
from myapp import app, db
from myapp.forms import LoginForm, RegistrationForm, EditProfileForm
from myapp.models import User


@app.before_request
def before_request():
    # No need to do db.session.add() because current_user from
    # Flask-Login will use load_user from models, and the user will
    # therefore already be in current session.
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


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
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
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


@app.route('/catalogue')
def catalogue():
    return render_template('index.html', title='Le Catalogue')


@app.route('/boulangerie')
def boulangerie():
    return render_template('index.html', title='Boulangerie')


@app.route('/patisserie')
def patisserie():
    return render_template('index.html', title='Patisserie')


@app.route('/bistro')
def bistro():
    return render_template('index.html', title='Bistro')


@app.route('/about')
def about():
    return render_template('index.html', title='About')


@app.route('/contactUs')
def contact_us():
    return render_template('index.html', title='Contact Us')


@app.route('/blog')
def le_blog():
    return render_template('index.html', title='Le Blog')


@app.route('/Admin')
@login_required
def admin():
    return render_template('index.html', title='Administration Hub')
