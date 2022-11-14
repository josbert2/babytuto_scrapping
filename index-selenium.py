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

    
db = mysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="babytuto"
)
today = date.today()
d1 = today.strftime("%d/%m/%Y")

workbook = xlrd.open_workbook("links.xlsx","rb")
sheets = workbook.sheet_names()
productos_link = []
for sheet_name in sheets:
    sh = workbook.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows):
        row_valaues = sh.row_values(rownum)
        productos_link.append(row_valaues[1])
def insert_links(links):
    cursor = db.cursor()
    cursor.execute('SELECT id_links FROM links')
    data = cursor.fetchall()
    cursor.close()
  
    if len(data) == len(links):
        print('[bold red] Links ya insertados [/bold red]')
     
    else:
        f.taskStatus(task='Insertando links en la base de datos', limit=5)
        for link in range(len(data), len(links)):
            cursor = db.cursor()
            cursor.execute("INSERT INTO links (links, id_links) VALUES (%s, %s)", (productos_link[link], link))
            db.commit()
            cursor.close()
        

insert_links(productos_link)


def checkElement(el):
    try:
        element = driver.find_element_by_css_selector(el)
        return 1
    except NoSuchElementException:
        return 0

executable_path = "./firefox"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
#driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
print("Current session is {}".format(driver.session_id))

cursor = db.cursor()
cursor.execute('SELECT * FROM productos')
data = cursor.fetchall()
cursor.close()

print('Hay un total de productos: ' + str(len(data)))

for i in range(len(data), len(productos_link)):
    print(f'[bold green] ✔ [/bold green] Escaneando URL: ' + str(i) + ' Link: ' + productos_link[i] + ' [bold green] Success [/bold green]')
  
    #options = Options()
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    #if platform == "win32":
    #    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
    #else:
    #    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
        #driver = webdriver.Chrome(executable_path='./chromedriver')
    #driver.set_window_position(0, 0)
    #options = Options()
    #options.add_argument("--window-size=1920x1080")
    #options.add_argument("--verbose")
    #options.add_argument("start-maximized")
    #driver = webdriver.Firefox(executable_path=executable_path)
    #driver.get(productos_link[i]) # Searched Character Page

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    try:
        #driver.get('https://www.babytuto.com/productos/libros-infantiles-libros-infantiles,timer-dental-angie,227656')
        #driver.get('https://www.babytuto.com/productos/cunas-de-madera,cuna-con-mudador-bambini-kidscool,148990?bt_f=home-hot')
        #driver.get('https://www.babytuto.com/productos/higiene-salud-portachupetes,porta-chupete-chevron-color-turquesa-me-mima,226842') # No se ve pero sirve
        #driver.get('https://www.babytuto.com/productos/ropa-y-zapatos-ajuar') # no sirve
        driver.get(productos_link[i])
    except Exception as e:
        print(e.message)
    

    time.sleep(2)
 
    if checkElement('.not-available-other') == 1 or checkElement('.alert-container') == 1:
        if checkElement('.alert-container') != 0:
            nombre = 'El producto no existe'
            print(f'[bold red] x [/bold red] No existe nombre [bold red] Failed [/bold red]')
            print('No hay nada que hacer')
            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (nombre, marca, descripcion, valoraciones, despachogratis, breadcrumb, categoria_principal, imagenprincipal, precionormal, preciooferta, tagbabyflash, tagbestseller, stockonline, stockbodega, scrap_id, url, producto_activo, date_scrapp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, i, productos_link[i], 0, str(d1)))
            db.commit()
            cursor.close()
        else:
            try:
                nombre = driver.find_element_by_css_selector('#product-information .title').text
                #NOMBRES.append(nombre)
                print(f'[bold green] ✔ [/bold green] Existe nombre [bold green] Success [/bold green]')
            except NoSuchElementException:
                #NOMBRES.append(0)
                nombre = 0
                print(f'[bold red] x [/bold red] No existe nombre [bold red] Failed [/bold red]')


            try:
                marca =  driver.find_element_by_css_selector('#product-information .merchant-name').text
                #MARCAS.append(marca)
                print(f'[bold green] ✔ [/bold green] Existe marca [bold green] Success [/bold green]')
            except NoSuchElementException:
                #MARCAS.append(0)
                marca = 0
                print(f'[bold red] x [/bold red] No existe marca [bold red] Failed [/bold red]')

            if checkElement('.ts-reviews-count') > 0:
                valoracion = driver.find_element_by_css_selector('.ts-reviews-count').text
                #VALORACIONES.append(valoracion)
                print(f'[bold green] ✔ [/bold green] Existe valoraciones [bold green] Success [/bold green]')
            else:
                #VALORACIONES.append(0)
                valoracion = 0
                print(f'[bold red] x [/bold red] No existe valoraciones [bold red] Failed [/bold red]')


            try: 
                precionormal = driver.find_element_by_css_selector('#product-information .original').text
                if precionormal == '':
                    #PRECIOS.append(0)
                    precionormal = 0
                else:
                    precionormal = driver.find_element_by_css_selector('#product-information .original').text
                    #PRECIOS.append(precionormal)
                print(f'[bold green] ✔ [/bold green] Existe precionormal [bold green] Success [/bold green]')
            except NoSuchElementException:
                #PRECIOS.append(0)
                precionormal = 0
                print(f'[bold red] x [/bold red] No existe precionormal [bold red] Failed [/bold red]')


            try: 
                preciooferta = driver.find_element_by_css_selector('#product-information .final').text
                #PRECIOOFERTA.append(preciooferta)
                print(f'[bold green] ✔ [/bold green] Existe preciooferta [bold green] Success [/bold green]')
            except NoSuchElementException:
                #PRECIOOFERTA.append(0)
                preciooferta = 0
                print(f'[bold red] x [/bold red] No existe preciooferta [bold red] Failed [/bold red]')
            

            try: 
                description = driver.find_element_by_css_selector('#product-information .subtitle').text
                #DESCRIPTION.append(description)
                print(f'[bold green] ✔ [/bold green] Existe description [bold green] Success [/bold green]')
            except NoSuchElementException:
                #DESCRIPTION.append(0)
                description = 0
                print(f'[bold red] x [/bold red] No existe description [bold red] Failed [/bold red]')


            try: 
                despachogratis = driver.find_element_by_css_selector('#product-information .free-shipping').text
                despachogratis = 1
                #DESPACHOGRATIS.append(despachogratis)
                print(f'[bold green] ✔ [/bold green] Existe despachogratis [bold green] Success [/bold green]')
            except NoSuchElementException:
                #DESPACHOGRATIS.append(0)
                despachogratis = 0
                print(f'[bold red] x [/bold red] No existe despachogratis [bold red] Failed [/bold red]')


            try: 
                imagenprincipal = driver.find_element_by_css_selector('.zoom-elv').get_attribute('src')
                #IMAGENPRINCIPAL.append(imagenprincipal)
                print(f'[bold green] ✔ [/bold green] Existe imagen principal [bold green] Success [/bold green]')
            except NoSuchElementException:
                #IMAGENPRINCIPAL.append(0)
                imagenprincipal = 0
                print(f'[bold red] x [/bold red] No existe imagen principal [bold red] Failed [/bold red]')


          
            """if checkElement('.tags a') > 0:
                #TAGBABYFLASH.append(1)
                tagbabyflash = 1
                print(f'[bold green] ✔ [/bold green] Existe tagbabyflash [bold green] Success [/bold green]')
            else:
                #TAGBABYFLASH.append(0)
                tagbabyflash = 0
                print(f'[bold red] x [/bold red] No existe tagbabyflash [bold red] Failed [/bold red]')

            #TAGBESTSELLER
           
            if checkElement('.tags .tag') > 0:
                if driver.find_element_by_css_selector('.tags a img').get_attribute('src') == '/logos/Babyflash.png':
                    #image = driver.find_element_by_css_selector('.tags img')[1]['src']
                    #TAGBESTSELLER.append(1)
                    tagbestseller = 1
                else:
                    #TAGBESTSELLER.append(0) 
                    tagbestseller = 0
            else:
                #TAGBESTSELLER.append(0)
                tagbestseller = 0
                print(f'[bold red] x [/bold red] No existe tagbestseller [bold red] Failed [/bold red]')
            """
       

            tags = driver.find_elements_by_css_selector('.span5.buy .details .tags img')
            tagbestseller = 0
            tagbabyflash = 0
            for tag in tags:
                if tag.get_attribute('src') == 'https://www.babytuto.com/logos/Babyflash.png':
                    tagbabyflash = 1
                    print(f'[bold green] ✔ [/bold green] Existe tagbabyflash [bold green] Success [/bold green]')
                if tag.get_attribute('src') == 'https://www.babytuto.com/logos/BESTSELLER.png':
                    tagbestseller = 1
                    print(f'[bold green] ✔ [/bold green] Existe tagbestseller [bold green] Success [/bold green]')
      
          
              

            if len(driver.find_elements_by_css_selector('.span5.buy .details .tags img')) > 0:
                print()
            else:
                tagbabyflash = 0
                tagbestseller = 0
         

            categorias = driver.find_elements_by_css_selector('.product .breadcrumb li')
            breadcrumbs = ''
            for li in categorias:
                breadcrumbs += li.text + ' '
            
           
            


            categoria_principal =  driver.find_element_by_css_selector('.product .breadcrumb li:last-child a').text
            #for ul in categorias:
            #    for li in ul:
            #        breadcrumbs += li

            if checkElement('.span5.buy .info .table') > 0:
                #STOCKONLINE.append(soup.select('.span5.buy .info .table tbody tr:nth-child(1) td:nth-child(2)')[0].text)
                stockonline = driver.find_element_by_css_selector('.span5.buy .info .table tbody tr:nth-child(1) td:nth-child(2)').text
                print(f'[bold green] ✔ [/bold green] Existe Stock online [bold green] Success [/bold green]')
            else:
                #STOCKONLINE.append(0)
                stockonline = 0
                print(f'[bold red] x [/bold red] No existe stock online [bold red] Failed [/bold red]')

            if checkElement('.span5.buy .info .table') > 0:
                #STOCKBODEGA.append(soup.select('.span5.buy .info .table tbody tr:nth-child(2) td:nth-child(2)')[0].text)
                stockbodega = driver.find_element_by_css_selector('.span5.buy .info .table tbody tr:nth-child(2) td:nth-child(2)').text
                print(f'[bold green] ✔ [/bold green] Existe Stock bodega [bold green] Success [/bold green]')
            else:
                #STOCKBODEGA.append(0)
                stockbodega = 0
                print(f'[bold red] x [/bold red] No existe stock bodega [bold red] Failed [/bold red]')

            
           


            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (nombre, marca, descripcion, valoraciones, despachogratis, breadcrumb, categoria_principal, imagenprincipal, precionormal, preciooferta, tagbabyflash, tagbestseller, stockonline, stockbodega, scrap_id, url, producto_activo, date_scrapp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre, marca, description, valoracion, despachogratis, breadcrumbs, categoria_principal, imagenprincipal, precionormal, preciooferta, tagbabyflash, tagbestseller, stockonline, stockbodega, i, productos_link[i], 0, str(d1)))
            db.commit()
            cursor.close()
        print('no paso')
    else:
        if checkElement('.not-available-other') == 1:
            print('no paso')
            nombre = driver.find_element_by_css_selector('#product-information .title').text
            print(f'[bold green] ✔ [/bold green] Existe nombre [bold green] Success [/bold green]')
            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (nombre, marca, descripcion, valoraciones, scrap_id, url, producto_activo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, 0, 0, 0, i, productos_link[i], 0))
            db.commit()
            cursor.close()
            print('hola 3')
        else:
            print('paso')

            try:
                nombre = driver.find_element_by_css_selector('#product-information .title').text
                #NOMBRES.append(nombre)
                print(f'[bold green] ✔ [/bold green] Existe nombre [bold green] Success [/bold green]')
            except NoSuchElementException:
                #NOMBRES.append(0)
                nombre = 0
                print(f'[bold red] x [/bold red] No existe nombre [bold red] Failed [/bold red]')


            try:
                marca =  driver.find_element_by_css_selector('#product-information .merchant-name').text
                #MARCAS.append(marca)
                print(f'[bold green] ✔ [/bold green] Existe marca [bold green] Success [/bold green]')
            except NoSuchElementException:
                #MARCAS.append(0)
                marca = 0
                print(f'[bold red] x [/bold red] No existe marca [bold red] Failed [/bold red]')

            if checkElement('.ts-reviews-count') > 0:
                valoracion = driver.find_element_by_css_selector('.ts-reviews-count').text
                #VALORACIONES.append(valoracion)
                print(f'[bold green] ✔ [/bold green] Existe valoraciones [bold green] Success [/bold green]')
            else:
                #VALORACIONES.append(0)
                valoracion = 0
                print(f'[bold red] x [/bold red] No existe valoraciones [bold red] Failed [/bold red]')


            try: 
                precionormal = driver.find_element_by_css_selector('#product-information .original').text
                if precionormal == '':
                    #PRECIOS.append(0)
                    precionormal = 0
                else:
                    precionormal = driver.find_element_by_css_selector('#product-information .original').text
                    #PRECIOS.append(precionormal)
                print(f'[bold green] ✔ [/bold green] Existe precionormal [bold green] Success [/bold green]')
            except NoSuchElementException:
                #PRECIOS.append(0)
                precionormal = 0
                print(f'[bold red] x [/bold red] No existe precionormal [bold red] Failed [/bold red]')


            try: 
                preciooferta = driver.find_element_by_css_selector('#product-information .final').text
                #PRECIOOFERTA.append(preciooferta)
                print(f'[bold green] ✔ [/bold green] Existe preciooferta [bold green] Success [/bold green]')
            except NoSuchElementException:
                #PRECIOOFERTA.append(0)
                preciooferta = 0
                print(f'[bold red] x [/bold red] No existe preciooferta [bold red] Failed [/bold red]')
            

            try: 
                description = driver.find_element_by_css_selector('#product-information .subtitle').text
                #DESCRIPTION.append(description)
                print(f'[bold green] ✔ [/bold green] Existe description [bold green] Success [/bold green]')
            except NoSuchElementException:
                #DESCRIPTION.append(0)
                description = 0
                print(f'[bold red] x [/bold red] No existe description [bold red] Failed [/bold red]')


            try: 
                despachogratis = driver.find_element_by_css_selector('#product-information .free-shipping').text
                despachogratis = 1
                #DESPACHOGRATIS.append(despachogratis)
                print(f'[bold green] ✔ [/bold green] Existe despachogratis [bold green] Success [/bold green]')
            except NoSuchElementException:
                #DESPACHOGRATIS.append(0)
                despachogratis = 0
                print(f'[bold red] x [/bold red] No existe despachogratis [bold red] Failed [/bold red]')


            try: 
                imagenprincipal = driver.find_element_by_css_selector('.zoom-elv').get_attribute('src')
                #IMAGENPRINCIPAL.append(imagenprincipal)
                print(f'[bold green] ✔ [/bold green] Existe imagen principal [bold green] Success [/bold green]')
            except NoSuchElementException:
                #IMAGENPRINCIPAL.append(0)
                imagenprincipal = 0
                print(f'[bold red] x [/bold red] No existe imagen principal [bold red] Failed [/bold red]')


          
            """if checkElement('.tags a') > 0:
                #TAGBABYFLASH.append(1)
                tagbabyflash = 1
                print(f'[bold green] ✔ [/bold green] Existe tagbabyflash [bold green] Success [/bold green]')
            else:
                #TAGBABYFLASH.append(0)
                tagbabyflash = 0
                print(f'[bold red] x [/bold red] No existe tagbabyflash [bold red] Failed [/bold red]')

            #TAGBESTSELLER
           
            if checkElement('.tags .tag') > 0:
                if driver.find_element_by_css_selector('.tags a img').get_attribute('src') == '/logos/Babyflash.png':
                    #image = driver.find_element_by_css_selector('.tags img')[1]['src']
                    #TAGBESTSELLER.append(1)
                    tagbestseller = 1
                else:
                    #TAGBESTSELLER.append(0) 
                    tagbestseller = 0
            else:
                #TAGBESTSELLER.append(0)
                tagbestseller = 0
                print(f'[bold red] x [/bold red] No existe tagbestseller [bold red] Failed [/bold red]')
            """
       

            tags = driver.find_elements_by_css_selector('.span5.buy .details .tags img')
            tagbestseller = 0
            tagbabyflash = 0
            for tag in tags:
                if tag.get_attribute('src') == 'https://www.babytuto.com/logos/Babyflash.png':
                    tagbabyflash = 1
                    print(f'[bold green] ✔ [/bold green] Existe tagbabyflash [bold green] Success [/bold green]')
                if tag.get_attribute('src') == 'https://www.babytuto.com/logos/BESTSELLER.png':
                    tagbestseller = 1
                    print(f'[bold green] ✔ [/bold green] Existe tagbestseller [bold green] Success [/bold green]')
      
          
              

            if len(driver.find_elements_by_css_selector('.span5.buy .details .tags img')) > 0:
                print()
            else:
                tagbabyflash = 0
                tagbestseller = 0
         

            categorias = driver.find_elements_by_css_selector('.product .breadcrumb li')
            breadcrumbs = ''
            for li in categorias:
                breadcrumbs += li.text + ' '
            
           
            


            categoria_principal =  driver.find_element_by_css_selector('.product .breadcrumb li:last-child a').text
            #for ul in categorias:
            #    for li in ul:
            #        breadcrumbs += li

            if checkElement('.span5.buy .info .table') > 0:
                #STOCKONLINE.append(soup.select('.span5.buy .info .table tbody tr:nth-child(1) td:nth-child(2)')[0].text)
                stockonline = driver.find_element_by_css_selector('.span5.buy .info .table tbody tr:nth-child(1) td:nth-child(2)').text
                print(f'[bold green] ✔ [/bold green] Existe Stock online [bold green] Success [/bold green]')
            else:
                #STOCKONLINE.append(0)
                stockonline = 0
                print(f'[bold red] x [/bold red] No existe stock online [bold red] Failed [/bold red]')

            if checkElement('.span5.buy .info .table') > 0:
                #STOCKBODEGA.append(soup.select('.span5.buy .info .table tbody tr:nth-child(2) td:nth-child(2)')[0].text)
                stockbodega = driver.find_element_by_css_selector('.span5.buy .info .table tbody tr:nth-child(2) td:nth-child(2)').text
                print(f'[bold green] ✔ [/bold green] Existe Stock bodega [bold green] Success [/bold green]')
            else:
                #STOCKBODEGA.append(0)
                stockbodega = 0
                print(f'[bold red] x [/bold red] No existe stock bodega [bold red] Failed [/bold red]')

            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (nombre, marca, descripcion, valoraciones, despachogratis, breadcrumb, categoria_principal, imagenprincipal, precionormal, preciooferta, tagbabyflash, tagbestseller, stockonline, stockbodega, scrap_id, url, producto_activo, date_scrapp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre, marca, description, valoracion, despachogratis, breadcrumbs, categoria_principal, imagenprincipal, precionormal, preciooferta, tagbabyflash, tagbestseller, stockonline, stockbodega, i, productos_link[i], 1, str(d1)))
            db.commit()
            cursor.close()

            """print(stockbodega)
            print(stockonline)
            print(breadcrumbs)
            print(nombre)
            print(marca)
            print(valoracion)
            print(precionormal)
            print(preciooferta)
            print(description)
            print(despachogratis)
            print(imagenprincipal)
            print(tagbabyflash)
            print(tagbestseller)"""