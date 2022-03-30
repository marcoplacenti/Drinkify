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

#Table Creation
cursor=conn.cursor()
create_table="""
create table if not exists Details (name varchar(200),email varchar(200),comment varchar(200),gender varchar(20) )
"""
cursor.execute(create_table)


def insert_details(name,email,comment,gender):
    cur=conn.cursor()
    cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)", (name,email,comment,gender))
    conn.commit()
    return

def get_details():
    cur=conn.cursor()
    cur.execute("SELECT * FROM Details")
    details = cur.fetchall()
    return details
