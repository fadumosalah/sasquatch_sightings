from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

# Sighting form
@app.route("/newsighting")
def newsighting():
    if "user_id" not in session:
        return redirect ('/')
    return render_template('add_sighting.html')

# adding sighting

@app.route('/create_sighting',methods=['POST'])
def create_sighting():
    if not Sighting.validate_sighting(request.form):
        return redirect("/newsighting")
    data ={
        "location" : request.form["location"],
        "description" : request.form["description"],
        "date" : request.form["date"],
        "amount" : request.form["amount"],
        "user_id" : session["user_id"],
    }
    Sighting.create_sighting(data)
    return redirect('/dashboard')

@app.route('/showsighting/<int:sighting_id>')
def show_sighting(sighting_id):
    data ={
        "id" : sighting_id
    }
    sighting = Sighting.get_sighting(data)
    return render_template("show.html", sighting= sighting)

@app.route ('/editsighting/<int:sighting_id>')
def edit_sighting(sighting_id):
    data ={
        "id" : sighting_id
    }
    sighting = Sighting.get_sighting(data)
    return render_template("edit.html", sighting= sighting)

@app.route ('/updatesighting/<int:sighting_id>', methods =["POST"])
def updatesighting(sighting_id):
    if not Sighting.validate_sighting(request.form):
        return redirect(f"/editsighting/{sighting_id}")
    Sighting.updatesighting(request.form, sighting_id)
    return redirect ('/dashboard')

@app.route("/deletesighting/<int:sighting_id>")
def deletesighting (sighting_id):
    data ={
        "id" : sighting_id
    }
    Sighting.delete_sighting(data)
    return redirect ('/dashboard')