# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020

@author: hp
"""

import pymysql
conn = pymysql.connect(
        host= 'drinkify-db.coewldes9avc.eu-north-1.rds.amazonaws.com', #endpoint link
        port = 3306, # 3306
        user = 'admin', # admin
        password = 'MyAdminPwd', #adminadmin
        db = 'drinkifydb', #test    
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
