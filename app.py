from flask import Flask,Response
from flask_restful import Resource, Api, reqparse
from datetime import datetime, timedelta
import time
import logging
import requests
import psycopg2
import nest_asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests_html import HTMLSession,AsyncHTMLSession
from benddao_func import check_db_auctions,get_data_from_url_element,insert_df_database,send_new_auct_email

app = Flask(__name__)
app.config['TIMEOUT'] = 300

@app.route('/')
def hello():
    return 'Hello from Flask!'

@app.route('/verif_auctions')
def verif_auctions():
    def generate():
        yield scrape()
    return Response(generate(),mimetype='text/plain')



def scrape():
    session = HTMLSession()
    url = "https://www.benddao.xyz/en/auctions/loans-in-auction/"
    website = "https://www.benddao.xyz/en/auctions/loans-in-auction/"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.ID,'__next')))
    #   driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source,'html.parser')

    pretty_html = soup.prettify()
    with open('new_res.html','w', encoding='utf-8') as f:
        f.write(pretty_html)
    f.close()
    driver.quit()
    
    
    return pretty_html


