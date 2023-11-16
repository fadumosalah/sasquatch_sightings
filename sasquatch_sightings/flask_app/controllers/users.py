from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask import flash
from flask_bcrypt import Bcrypt 

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.register(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_email(request.form)
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user = User.get_one(data), all = Sighting.get_all(), all_sightors = Sighting.get_sightings_with_users(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect ("/")

#@app.route('/dashboard')
#def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user = User.get_one(data), all = Sighting.get_sightings_with_users(data))