import datetime
import nest_asyncio
import logging
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
import os
import time
from os import listdir
from os.path import isfile, join
import asyncio
from requests_html import HTMLSession,AsyncHTMLSession
from selenium import webdriver
import pandas
import sqlite3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#this piece of code will be a function to take an a element and return data of the element bid
def get_data_from_url_element(a_elem):
    bid_detail = {}
    # a_elem = href_list[7]
    bid_block = a_elem.find_parent().find_parent().find_parent()
    try:
        bid_detail["url"] = bid_block.a["href"]
    except Exception:
        bid_detail["url"] = None
    try:
        bid_detail["name"] = bid_block.find_all('div',recursive=False)[1].get_text()
    except:
        bid_detail["name"] = None
    try:
        bid_detail["floor_price"] = bid_block.find_all('div',recursive=False)[2].div.find('span').get_text()
    except:
        bid_detail["floor_price"] = None
    try:
        bid_detail["debt"] = bid_block.find_all('div',recursive=False)[2].div.find_all('div',recursive=False)[2].find('span').get_text()
    except:
        bid_detail["debt"] = None
    try:
        bid_detail["auction_ends"] = bid_block.find_all('div',recursive=False)[2].div.find_all('div',recursive=False)[5].get_text()
    except:
        bid_detail["auction_ends"] = None
    try:    
        bid_detail["latest_bid"] = bid_block.find_all('div',recursive=False)[2].div.find_all('div',recursive=False)[6].get_text()
    except:
        bid_detail["latest_bid"] = None
    return bid_detail



def insert_df_database(df):
    conn = sqlite3.connect('benddao.db')
    c = conn.cursor()

    # CREATE TABLE "auctions" (
    # "url" TEXT,
    #   "name" TEXT,
    #   "floor_price" TEXT,
    #   "debt" TEXT,
    #   "auction_ends" TEXT,
    #   "latest_bid" TEXT
    # , IndexSeq INTEGER);

    c.execute('''CREATE TABLE IF NOT EXISTS auctions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        name TEXT,
        floor_price TEXT,
        debt TEXT,
        auction_ends TEXT,
        latest_bid TEXT,
        email_sent TEXT DEFAULT 0
        ) ''')

    for row in df.itertuples(index=False):
        c.execute("SELECT * FROM auctions WHERE NAME=?", (row.name,))
        result = c.fetchone()
        
        if result is None:
            c.execute("INSERT INTO auctions (url,name,floor_price,debt,auction_ends,latest_bid) VALUES (?,?,?,?,?,?)", (row.url,row.name,row.floor_price,row.debt,row.auction_ends,row.latest_bid))
        else:
            print("row exists with name " +row.name)
    conn.commit()
    conn.close()

def check_db_auctions():
    conn = sqlite3.connect('benddao.db')
    d_row = pandas.read_sql_query("SELECT * FROM auctions where email_sent=0",conn)
    
    c = conn.cursor()
    c.execute('''update auctions set email_sent=1 where email_sent=0''')
    conn.commit()
    conn.close()
    
    if d_row.empty:
        return None
    else:
        message = d_row.to_string()
        return message
    

def send_new_auct_email(recipient,message):
    sender = 'benddao@gmail.com'
    password = 'rylkulbqcazylohv'
    # recipient = 'jeanpierre1934@gmail.com'
    subject = 'Auctions Available'
 

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message,'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        # with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        # smtp.starttls()
        smtp.login(sender, password)
        smtp.sendmail(sender, recipient, msg.as_string())
    
    print('EMAIL sent success')
    return "ok"