from drinkify import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods = ['post'])
def insert():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['optradio']
        comment = request.form['comment']
        db.insert_details(name,email,comment,gender)
        return render_template('index.html')