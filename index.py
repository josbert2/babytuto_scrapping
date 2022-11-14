
import mysql.connector as mysql
import openpyxl
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from rich import print, pretty
import functions as f
import requests
import urllib.request

from  bs4 import BeautifulSoup
import xlrd


#Variables

NOMBRES = [] #✔
URLS = [] #✔
DESCRIPTION = [] #✔
MARCAS = [] #✔
PRECIOS = [] #✔
PRECIOOFERTA = [] #✔
CATEGORIA = [] #✔
CATEGORIA_PRINCIPAL = [] #✔
VALORACIONES = [] #✔
STOCKONLINE = [] #✔
STOCKBODEGA = [] #✔
IMAGENPRINCIPAL = [] #✔
IMAGENES = [] #X
TAGBABYFLASH = [] #✔
TAGBESTSELLER = [] #✔
DESPACHOGRATIS = []

def checkElement(el):
    el = len(el)
    if el > 0:
        return 1
    else:
        return 0


#f.taskStatus(task='Extract Info from Excel', limit=5)
#print(f'[bold red] x [/bold red] Precio normal NO encontrado [bold red] Failed [/bold red]')


db = mysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="babytuto"
)


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




cursor = db.cursor()
cursor.execute('SELECT * FROM productos')
data = cursor.fetchall()
cursor.close()

print('Hay un total de productos: ' + str(len(data)))

for i in range(len(data), len(productos_link)):
    print(f'[bold green] ✔ [/bold green] Escaneando URL: ' + str(i) + ' Link: ' + productos_link[i] + ' [bold green] Success [/bold green]')
    #URL = 'https://www.babytuto.com/productos/libros-infantiles-libros-paternidad,libro-recetas-para-mi-bebe,164360?bt_f=home-trending'
    URL = productos_link[i]
    from requests_html import HTMLSession
    s = HTMLSession()
    response = s.get(URL)
    response.html.render(timeout=550)
    #s.close()
    #response.close()

    print(response)
   
    #URLS.append(URL)

    #r = requests.get(URL)
    #html=r.text
    html = response.html.html
    soup = BeautifulSoup(html, 'html.parser')
    print(len(soup.select('#product-information')) != 0)



    if len(soup.select('#product-information')) != 1:
        if str(len(soup.select('.alert-container'))) == '0':
            nombre = 'El producto no existe'
            print(f'[bold red] x [/bold red] No existe nombre [bold red] Failed [/bold red]')
        else:
            nombre = soup.select('#product-information .title')[0].text
            print(f'[bold green] ✔ [/bold green] Existe nombre [bold green] Success [/bold green]')
    
        cursor = db.cursor()
        cursor.execute("INSERT INTO productos (nombre, marca, descripcion, valoraciones, scrap_id, url, producto_activo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, 0, 0, 0, i, productos_link[i], 0))
        db.commit()
        cursor.close()
        print('no paso')
    else:
        # Check container of product

        if len(soup.select('.not-available-other')) == 1:
            nombre = soup.select('#product-information .title')[0].text
            print(f'[bold green] ✔ [/bold green] Existe nombre [bold green] Success [/bold green]')
            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (nombre, marca, descripcion, valoraciones, scrap_id, url, producto_activo) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, 0, 0, 0, i, productos_link[i], 0))
            db.commit()
            cursor.close()
            print('no paso')
        else:
            print('paso')
        
            
        

            try:
                soup.find('div', {'id': 'product-information'})
                print(f'[bold green] ✔ [/bold green] Existe contenedor [bold green] Success [/bold green]')
            except NoSuchElementException:
                print(f'[bold red] x [/bold red] No existe contenedor [bold red] Failed [/bold red]')



            try:
                nombre = soup.select('#product-information .title')[0].text
                #NOMBRES.append(nombre)
                print(f'[bold green] ✔ [/bold green] Existe nombre [bold green] Success [/bold green]')
            except NoSuchElementException:
                #NOMBRES.append(0)
                nombre = 0
                print(f'[bold red] x [/bold red] No existe nombre [bold red] Failed [/bold red]')



            try:
                marca = soup.select('#product-information .merchant-name')[0].text
                #MARCAS.append(marca)
                print(f'[bold green] ✔ [/bold green] Existe marca [bold green] Success [/bold green]')
            except NoSuchElementException:
                #MARCAS.append(0)
                marca = 0
                print(f'[bold red] x [/bold red] No existe marca [bold red] Failed [/bold red]')



            if checkElement(soup.select('.ts-reviews-count')) > 0:
                valoracion = soup.select('.ts-reviews-count')[0].text
                #VALORACIONES.append(valoracion)
                print(f'[bold green] ✔ [/bold green] Existe valoraciones [bold green] Success [/bold green]')
            else:
                #VALORACIONES.append(0)
                valoracion = 0
                print(f'[bold red] x [/bold red] No existe valoraciones [bold red] Failed [/bold red]')

            try: 
                precionormal = soup.select('#product-information .original')[0].text
                if precionormal == '':
                    #PRECIOS.append(0)
                    precionormal = 0
                else:
                    precionormal = soup.select('#product-information .original')[0].text
                    #PRECIOS.append(precionormal)
                print(f'[bold green] ✔ [/bold green] Existe precionormal [bold green] Success [/bold green]')
            except NoSuchElementException:
                #PRECIOS.append(0)
                precionormal = 0
                print(f'[bold red] x [/bold red] No existe precionormal [bold red] Failed [/bold red]')


            try: 
                preciooferta = soup.select('#product-information .final')[0].text
                #PRECIOOFERTA.append(preciooferta)
                print(f'[bold green] ✔ [/bold green] Existe preciooferta [bold green] Success [/bold green]')
            except NoSuchElementException:
                #PRECIOOFERTA.append(0)
                preciooferta = 0
                print(f'[bold red] x [/bold red] No existe preciooferta [bold red] Failed [/bold red]')


            try: 
                description = soup.select('#product-information .subtitle')[0].text
                #DESCRIPTION.append(description)
                print(f'[bold green] ✔ [/bold green] Existe description [bold green] Success [/bold green]')
            except NoSuchElementException:
                #DESCRIPTION.append(0)
                description = 0
                print(f'[bold red] x [/bold red] No existe description [bold red] Failed [/bold red]')



            try: 
                despachogratis = soup.select('#product-information .free-shipping')[0].text
                despachogratis = 1
                #DESPACHOGRATIS.append(despachogratis)
                print(f'[bold green] ✔ [/bold green] Existe despachogratis [bold green] Success [/bold green]')
            except NoSuchElementException:
                #DESPACHOGRATIS.append(0)
                despachogratis = 0
                print(f'[bold red] x [/bold red] No existe despachogratis [bold red] Failed [/bold red]')


            try: 
                imagenprincipal = soup.select('.zoom-elv')[0]['src']
                #IMAGENPRINCIPAL.append(imagenprincipal)
                print(f'[bold green] ✔ [/bold green] Existe imagen principal [bold green] Success [/bold green]')
            except NoSuchElementException:
                #IMAGENPRINCIPAL.append(0)
                imagenprincipal = 0
                print(f'[bold red] x [/bold red] No existe imagen principal [bold red] Failed [/bold red]')



            

            # TAGBABYFLASH
            if checkElement(soup.select('.tags a')) > 0:
                #TAGBABYFLASH.append(1)
                tagbabyflash = 1
                print(f'[bold green] ✔ [/bold green] Existe tagbabyflash [bold green] Success [/bold green]')
            else:
                #TAGBABYFLASH.append(0)
                tagbabyflash = 0
                print(f'[bold red] x [/bold red] No existe tagbabyflash [bold red] Failed [/bold red]')

            #TAGBESTSELLER
            if checkElement(soup.select('.tags .tag')) > 0:
                if len(soup.select('.tags img')) == 2:
                    image = soup.select('.tags img')[1]['src']
                    #TAGBESTSELLER.append(1)
                    tagbestseller = 1
                else:
                    #TAGBESTSELLER.append(0) 
                    tagbestseller = 0
            else:
                #TAGBESTSELLER.append(0)
                tagbestseller = 0
                print(f'[bold red] x [/bold red] No existe tagbestseller [bold red] Failed [/bold red]')

            categorias = soup.select('.product .breadcrumb')[0].text
            breadcrumbs = ''
            for ul in categorias:
                for li in ul:
                    breadcrumbs += li
            print(breadcrumbs)
          

            categoria_principal =  soup.select('.product .breadcrumb li:last-child a')[0].text
            #CATEGORIA_PRINCIPAL.append(categoria_principal)


            if checkElement(soup.select('.span5.buy .info .table')) > 0:
                #STOCKONLINE.append(soup.select('.span5.buy .info .table tbody tr:nth-child(1) td:nth-child(2)')[0].text)
                stockonline = soup.select('.span5.buy .info .table tbody tr:nth-child(1) td:nth-child(2)')[0].text
                print(f'[bold green] ✔ [/bold green] Existe Stock online [bold green] Success [/bold green]')
            else:
                #STOCKONLINE.append(0)
                stockonline = 0
                print(f'[bold red] x [/bold red] No existe stock online [bold red] Failed [/bold red]')


            if checkElement(soup.select('.span5.buy .info .table')) > 0:
                #STOCKBODEGA.append(soup.select('.span5.buy .info .table tbody tr:nth-child(2) td:nth-child(2)')[0].text)
                stockbodega = soup.select('.span5.buy .info .table tbody tr:nth-child(2) td:nth-child(2)')[0].text
                print(f'[bold green] ✔ [/bold green] Existe Stock bodega [bold green] Success [/bold green]')
            else:
                #STOCKBODEGA.append(0)
                stockbodega = 0
                print(f'[bold red] x [/bold red] No existe stock bodega [bold red] Failed [/bold red]')


            cursor = db.cursor()
            cursor.execute("INSERT INTO productos (nombre, marca, descripcion, valoraciones, despachogratis, breadcrumb, categoria_principal, imagenprincipal, precionormal, preciooferta, tagbabyflash, tagbestseller, stockonline, stockbodega, scrap_id, url, producto_activo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (nombre, marca, description, valoracion, despachogratis, breadcrumbs, categoria_principal, imagenprincipal, precionormal, preciooferta, tagbabyflash, tagbestseller, stockonline, stockbodega, i, productos_link[i], 1))
            db.commit()
            cursor.close()







