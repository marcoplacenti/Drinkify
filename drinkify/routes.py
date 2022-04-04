from drinkify import app
from flask import render_template, request, redirect, url_for
from drinkify import db
import time

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



test = ((1, 'Water', 100, '1649070379.648753'), (1, 'Water', 100, '1649070426.912624'), (1, 'Water', 100, '1649070607.295744'), (1, 'Water', 100, '1649070647.2487102'), (1, 'Water', 100, '1649070702.4659996'), (1, 'Water', 100, '1649070723.6206126'), (1, 'Water', 100, '1649070834.7059758'), (1, 'Water', 100, '1649071127.0913403'))

@app.route('/drink', methods = ['get', 'post'])
def drink():
    data = db.get_drinks()
    total = 0
    send_data = []
    print(data)
    for row in data:
        d = {
            "drink": row[1],
            "amount": row[2],
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[3])))
        }
        total += int(row[2])
        send_data.append(d)
    
    goal = 2000
    progress = str(min(100, int((total/goal)*100)))

    if request.method == 'POST':
        userID = 1
        drink = request.form['drink']
        amount = request.form['amount']
        timestamp = str(time.time())
        db.insert_drink(userID, drink, amount, timestamp)
        return redirect(url_for('drink'))
    
    return render_template('drink.html', data=send_data, progress=progress, total=total) 
    
@app.route('/visuals')
def visuals():
    return render_template('visuals.html')