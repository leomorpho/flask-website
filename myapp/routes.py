from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user,  \
        login_required
from werkzeug.urls import url_parse
from myapp import app, db
from myapp.forms import LoginForm, RegistrationForm
from myapp.models import User

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Leo'}
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
