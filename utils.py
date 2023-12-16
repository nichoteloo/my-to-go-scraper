import os
import csv
import time
import random
import logging
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, Timeout

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
PROXIES_REQUIRED = os.getenv("PROXIES_REQUIRED").lower() == "true"
PROXIES = []

class ScrapingException(Exception):
    pass

def _time_sleep(sec=5):
    for i in range(sec):
        print("Sleeping for {} seconds".format(sec - i))
        time.sleep(1)

def make_request(url, return_type="page"):
    try:
        r = requests.get(url, timeout=10)
    except Exception as re:
        logging.warning(u"Request failed or timeout, trying again in 5 seconds: {}".format(re))
        _time_sleep(5)
        return make_request(url, return_type=return_type)
    
    if return_type == "page":
        return BeautifulSoup(r.text, "html.parser")
    elif return_type == "text":
        return r.text
    elif return_type == "respose":
        return r

def get_proxy():
    pass

def no_proxies():
    pass