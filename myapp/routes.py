from flask import render_template, flash, redirect, url_for
from myapp import app
from myapp.forms import LoginForm

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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

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
