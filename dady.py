from PIL import Image, ImageDraw, ImageFont
import textwrap
import qrcode

import mysql.connector as mysql

from openpyxl import Workbook
import xlrd
import requests
from io import BytesIO
from random import randrange

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import InvalidSessionIdException



from time import sleep
import time
from alive_progress import alive_bar, config_handler
from rich import print
from rich.console import Console
import sys
from datetime import date



from selenium.common.exceptions import NoSuchElementException
from sys import platform



executable_path = "./firefox"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
#driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
print("Current session is {}".format(driver.session_id))

HASH = 'Qid=0c044bf4-e20c-4ad8-a857-965202210400&Cid=es-CL&f=0'
for i in range(100):


    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver.execute_script("window.open('about:blank','secondtab');")
    driver.switch_to.window("secondtab")
    driver.get('https://queue.puntoticket.com/?c=puntoticket&e=biz188b&cid=es-CL&t_cal=1&t_ct=2')
   
 
  