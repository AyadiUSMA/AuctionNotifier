from flask import Flask
from flask_restful import Resource, Api, reqparse
from datetime import datetime, timedelta
import logging
import requests
import psycopg2
from benddao_func import check_db_auctions,get_data_from_url_element,insert_df_database,send_new_auct_email

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello from Flask!'

@app.route('/verif_auctions')
def verif_auctions():
    session = HTMLSession()
    nest_asyncio.apply()
    url = "https://www.benddao.xyz/en/auctions/loans-in-auction/"
    website = "https://www.benddao.xyz/en/auctions/loans-in-auction/"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(15)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.ID,'__next')))
    #   driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source,'html.parser')

    pretty_html = soup.prettify()
    with open('new_res.html','w', encoding='utf-8') as f:
        f.write(pretty_html)
    f.close()
    driver.quit()
    return "ok"


