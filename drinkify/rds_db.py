# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020

@author: hp
"""

import pymysql
import yaml

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
    water_amount float,
    time varchar(100),
    location varchar(100)
)
"""
#cursor.execute("drop table if exists drink_logs")
cursor.execute(drink_table)



def delete_history():
    cur = conn.cursor()
    cursor.execute("truncate drink_logs")

def insert_drink(userID, drink_id, drink, amount, time, location):
    water_amount = None
    if drink == 'Water':
        water_amount = amount
    elif drink == 'Coffee':
        water_amount = str(int(amount)*0.5)
    elif drink == 'Beer':
        water_amount = str(int(amount)*0.1)

    cur=conn.cursor()
    cur.execute("INSERT INTO drink_logs (userID, drink_id, drink, amount, water_amount, time, location) VALUES (%s,%s,%s,%s,%s,%s,%s)", (userID, drink_id, drink, amount, water_amount, time, location))
    conn.commit()

def get_drinks():
    cur=conn.cursor()
    cur.execute("SELECT * FROM drink_logs")
    drinks = cur.fetchall()
    return drinks