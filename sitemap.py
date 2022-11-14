import requests
from bs4 import BeautifulSoup
import pandas as pd
  



url = 'https://www.babytuto.com/sitemap/products.xml'
data = []
soup = BeautifulSoup(requests.get(url).text, 'lxml')

for loc in soup.select('url > loc'):
    data.append(loc.text)

cars_data = pd.DataFrame({'urls': data})
datatoexcel = pd.ExcelWriter('CarsData1.xlsx')
  
# write DataFrame to excel
cars_data.to_excel(datatoexcel)
  
# save the excel
datatoexcel.save()