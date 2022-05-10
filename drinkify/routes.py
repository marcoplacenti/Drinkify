from drinkify import app
from flask import render_template, request, redirect, jsonify, url_for
from drinkify import db
import time
import pandas as pd
import uuid
from datetime import datetime, date


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
    
    left_to_go = max(0, int(goal) - total)
    
    if request.method == 'POST':
        userID = 1
        drink_id = uuid.uuid1()
        drink = request.form['drink']
        amount = request.form['amount']
        timestamp = request.form['logTime']
        location = request.form['location']
        db.insert_drink(userID, drink_id, drink, amount, timestamp, location)

        return redirect(url_for('drink'))
    df_today['hourminute'] = df_today['timestamp'].dt.strftime('%H:%M')
    df_today['timestamp'] = df_today['timestamp'].dt.strftime('%Y-%m-%d')
    print(len(df_today))
    if len(df_today) == 0:
        d = {
            "hourminute": "Go",
            "drink": "get",
            "amount": "yourself",
            "water_amount": "a",
            "location": "drink"
        }
        df_today = pd.DataFrame([d])
    return render_template('drink.html', data=send_data, progress=progress, total=total, left_to_go=left_to_go, datatoday = df_today.to_dict(orient='records')) 

@app.route('/settings')
def settings():
    goal = db.get_goal()
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
    return render_template('settings.html', goal=goal, data=send_data)

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
            "water_amount": row[4],
            "timestamp": row[5],
            "location": row[6]
        }
        df.append(d)
    df = pd.DataFrame(df)
    df.timestamp = df.timestamp.apply(pd.to_datetime)
    # df_hour = df.groupby(pd.Grouper(key="timestamp", freq="H")).sum()
    # df_hour = df_hour.reset_index()
    # df_hour['hour'] = df_hour.timestamp.dt.hour
    goal = db.get_goal()
    return render_template('visuals.html', data = df.to_json(orient='records'), goal = goal)
