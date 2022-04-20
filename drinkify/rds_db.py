# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020

@author: hp
"""

import pymysql
import yaml
import datetime
from datetime import date


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
    drink ENUM('Water', 'Coffee', 'Beer'),
    amount int, 
    water_amount int,
    timestamp varchar(100),
    location varchar(100)
)
"""
#cursor.execute("drop table if exists drink_logs")
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



def delete_history():
    cur=conn.cursor()
    cur.execute("truncate drink_logs")
    conn.commit()

def insert_drink(userID, drink_id, drink, amount, time, location):
    water_amount = None
    if drink == 'Water':
        water_amount = amount
    elif drink == 'Coffee':
        water_amount = str(int(amount)*0.5)
    elif drink == 'Beer':
        water_amount = str(int(amount)*0.1)

    timestamp = str(date.today()) + ' ' + time
    #timestamp = datetime.strptime(today, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M')

    cur=conn.cursor()
    cur.execute("INSERT INTO drink_logs (userID, drink_id, drink, amount, water_amount, timestamp, location) VALUES (%s,%s,%s,%s,%s,%s,%s)", (userID, drink_id, drink, amount, water_amount, timestamp, location))
    conn.commit()

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