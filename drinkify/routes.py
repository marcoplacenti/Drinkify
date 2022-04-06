from drinkify import app
from flask import render_template, request, redirect, url_for
from drinkify import db
import time
import pandas as pd
import uuid


#test = ((1, 'Water', 100, '1649070379.648753'), (1, 'Water', 100, '1649070426.912624'), (1, 'Water', 100, '1649070607.295744'), (1, 'Water', 100, '1649070647.2487102'), (1, 'Water', 100, '1649070702.4659996'), (1, 'Water', 100, '1649070723.6206126'), (1, 'Water', 100, '1649070834.7059758'), (1, 'Water', 100, '1649071127.0913403'))

@app.route('/')
def main():
    return redirect("/drink", code=302)

@app.route('/drink', methods = ['get', 'post'])
def drink():
    data = db.get_drinks()
    print(data)
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

        total += d['water_amount']
        send_data[-i-1] = d
    
    goal = 2000
    progress = str(min(100, int((total/goal)*100)))

    if request.method == 'POST':
        userID = 1
        drink_id = uuidOne = uuid.uuid1()
        drink = request.form['drink']
        amount = request.form['amount']
        timestamp = request.form['timestamp']
        location = request.form['location']
        db.insert_drink(userID, drink_id, drink, amount, timestamp, location)

        return redirect(url_for('drink'))
    
    return render_template('drink.html', data=send_data, progress=progress, total=total) 

@app.route('/clear')
def clear_history():
    db.delete_history()
    return redirect("/drink", code=302)
    
@app.route('/visuals')
def visuals():

    # data = db.get_drinks()
    # df = []
    # for row in data:
    #     d = {
    #         "drink": row[1],
    #         "amount": row[2],
    #         "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(row[3])))
    #     }
    #     df.append(d)
    # df = pd.DataFrame(df)
    # df.timestamp = df.timestamp.apply(pd.to_datetime)
    
    # df.to_csv(r'C:\Users\morte\OneDrive\Dokumenter\GitHub\Drinkify\test.csv')

    # df_hour = df.groupby(pd.Grouper(key="timestamp", freq="H")).sum()
    # df_hour = df_hour.reset_index()
    # df_hour['hour'] = df_hour.timestamp.dt.hour

    #return render_template('visuals.html', data=df_hour.to_json(orient='records'))
    return "OK"