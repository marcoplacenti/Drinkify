# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020

@author: hp
"""

import pymysql
import yaml
from random import randrange
from datetime import date,timedelta, datetime
import uuid
import random
random.seed(42)

with open('.credentials.yml') as infile:
    cred = yaml.load(infile, Loader=yaml.SafeLoader)
    host = cred['host']
    user = cred['user']
    pwd = cred['password']
    db = cred['database']

conn = pymysql.connect(
        host= host,
        port = 3306,
        user = user,
        password = pwd,
        db = db
        )

cursor=conn.cursor()
drink_table = """

create table if not exists drink_logs(
    userID int,
    drink_id varchar(100),
    drink ENUM('Water', 'Coffee', 'Beer', 'Wine', 'Soda', 'Tea', 'Juice', 'Milk'),
    amount int, 
    water_amount int,
    timestamp varchar(100),
    location varchar(100)
)
"""
cursor.execute("drop table if exists drink_logs")
cursor.execute(drink_table)

#cursor.execute("drop table if exists goals")
goal_table = """
create table if not exists goals(
    user_id varchar(15) default 1,
    goal int default 2000
);
"""
cursor.execute(goal_table)
conn.commit()

### POPULATE TABLE ###
start_date = date(2022, 2, 20)
end_date = date(2022, 4, 20)

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    random_date = random_date.strftime('%Y-%m-%d')
    time = timedelta(hours=random.randint(9,23), minutes=random.randint(0,59))
    random_date += " " + str(time)[:-3]
    return random_date

def water_amount_calc(drink, amount):
    water_amount = None
    if drink == 'Water':
        water_amount = amount
    elif drink == 'Coffee':
        water_amount = str(int(amount)*0.9875)
    elif drink == 'Beer':
        water_amount = str(int(amount)*0.95)
    elif drink == 'Wine':
        water_amount = str(int(amount)*0.85)
    elif drink == 'Soda':
        water_amount = str(int(amount)*0.90)
    elif drink == 'Tea':
        water_amount = str(int(amount)*0.99)
    elif drink == 'Juice':
        water_amount = str(int(amount)*0.90)
    elif drink == 'Milk':
        water_amount = str(int(amount)*0.87)
    return water_amount

def tablerow():
    userID = "1"
    drink_id = f"{uuid.uuid1()}"
    drink = random.choice(['Water','Water','Water','Water','Water', 'Coffee','Coffee','Coffee', 
                            'Beer','Beer','Beer', 'Wine', 'Soda','Soda', 'Tea', 'Juice', 'Milk'])
    amount = random.choice(['50', '100', '200', '300', '300', '500'])
    water_amount = water_amount_calc(drink, amount)
    date = random_date(start_date, end_date)
    location = random.choice(['Home', 'Restaurant', 'Work','School'])
    return (userID, f'{drink_id}', f'{drink}', amount, water_amount, f'{date}', f'{location}')

def query_text(number_of_reps):
    s = ""
    for i in range(number_of_reps):
        s += str(tablerow())
        s += ", "
    return s[:-2] + ";"

query = f"""
INSERT INTO drink_logs (userID, drink_id, drink, amount, water_amount, timestamp, location) VALUES
    {query_text(600)}
"""

cursor.execute(query)
conn.commit()

def delete_history():
    cur=conn.cursor()
    cur.execute("truncate drink_logs")
    conn.commit()

def insert_drink(userID, drink_id, drink, amount, time, location):
    water_amount = water_amount_calc(drink, amount)

    timestamp = str(date.today()) + ' ' + time
    #timestamp = datetime.strptime(today, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M')

    cur=conn.cursor()
    cur.execute("INSERT INTO drink_logs (userID, drink_id, drink, amount, water_amount, timestamp, location) VALUES (%s,%s,%s,%s,%s,%s,%s)", (userID, drink_id, drink, amount, water_amount, timestamp, location))
    conn.commit()
    print((userID, drink_id, drink, amount, water_amount, timestamp, location))

def get_drinks():
    cur=conn.cursor()
    cur.execute("SELECT * FROM drink_logs")
    drinks = cur.fetchall()
    conn.commit()
    return drinks

def is_goal_set():
    cur = conn.cursor()
    cur.execute("select goal from goals where user_id = 1")
    goal = cur.fetchone()
    conn.commit()
    return goal

def get_goal():
    goal = is_goal_set()
    if goal is not None:
        return goal[0]
    else:
        cur = conn.cursor()
        cur.execute("insert into goals (user_id, goal) values (1, 2000)")
        conn.commit()
        return 2000

def set_goal(goal):
    cur = conn.cursor()
    cur.execute("update goals set goal = "+str(int(goal))+" where user_id = 1")
    conn.commit()