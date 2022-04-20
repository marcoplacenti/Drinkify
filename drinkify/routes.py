from drinkify import app
from flask import render_template, request, redirect, jsonify, url_for
from drinkify import db
import time
import pandas as pd
import uuid
from datetime import datetime, date


#test = ((1, 'Water', 100, '1649070379.648753'), (1, 'Water', 100, '1649070426.912624'), (1, 'Water', 100, '1649070607.295744'), (1, 'Water', 100, '1649070647.2487102'), (1, 'Water', 100, '1649070702.4659996'), (1, 'Water', 100, '1649070723.6206126'), (1, 'Water', 100, '1649070834.7059758'), (1, 'Water', 100, '1649071127.0913403'))

@app.route('/')
def main():
    return redirect("/drink", code=302)

@app.route('/drink', methods = ['get', 'post'])
def drink():
    data = db.get_drinks()
    #print(data)
    total = 0
    l = len(data)
    send_data = [None] * l
    for i, row in enumerate(data):
        d = {
            "drink": row[2],
            "amount": row[3],
            "water_amount": row[4],
            "timestamp": row[5],
            "location": row[6]
        }

        send_data[-i-1] = d #flip the order so the table is from new to old

    df = pd.DataFrame(send_data)
    df.timestamp = pd.to_datetime(df.timestamp)
    
    # filter the progress by today
    today = pd.Timestamp('today')
    mask = (df.timestamp.dt.date == today)
    df_today = df[mask]

    total = df_today.water_amount.sum()
    goal = db.get_goal()

    progress = str(min(100, int((total/goal)*100)))
    
    if request.method == 'POST':
        userID = 1
        drink_id = uuid.uuid1()
        drink = request.form['drink']
        amount = request.form['amount']
        timestamp = request.form['logTime']
        location = request.form['location']
        db.insert_drink(userID, drink_id, drink, amount, timestamp, location)

        return redirect(url_for('drink'))
    
    return render_template('drink.html', data=send_data, progress=progress, total=total) 

@app.route('/clear', methods = ['get', 'post'])
def clear_history():
    db.delete_history()
    return redirect("/drink", code=302)

@app.route('/setGoal', methods = ['get', 'post'])
def set_goal():
    if request.method == 'POST':
        goal = request.form['goal']
        db.set_goal(goal)
    return redirect("/drink", code=302)

# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4207053/
@app.route('/calcGoal', methods=['get', 'post'])
def calc_goal():
    if request.method == 'POST':
        sex = request.form['sex']
        age = request.form['age']

        if sex == 'male':
            if age == '14-18':
                goal = 3300 * 0.75
            if age == '19+':
                goal = 3700 * 0.75
        if sex == 'female':
            if age == '14-18':
                goal = 2300 * 0.75
            if age == '19+':
                goal = 2700 * 0.75

        db.set_goal(int(goal))
        return render_template('settings.html', goal=int(goal))
    
@app.route('/visuals')
def visuals():

    data = db.get_drinks()
    df = []
    for row in data:
        d = {
            "drink": row[2],
            "amount": row[3],
            "timestamp": row[5],
            "location": row[6]
        }
        df.append(d)
    df = pd.DataFrame(df)
    df.timestamp = df.timestamp.apply(pd.to_datetime)
    # df_hour = df.groupby(pd.Grouper(key="timestamp", freq="H")).sum()
    # df_hour = df_hour.reset_index()
    # df_hour['hour'] = df_hour.timestamp.dt.hour
    return render_template('visuals.html', data = df.to_json(orient='records', date_format='iso'))


@app.route('/settings')
def settings():
    goal = db.get_goal()
    return render_template('settings.html', goal=goal)
