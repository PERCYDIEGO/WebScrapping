import csv
import requests
from bs4 import BeautifulSoup
import schedule
import time
import pandas as pd
import numpy as np
from time import sleep
from datetime import datetime


# add your user agent 
HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 
'Accept-Language': 'es, es-ES;q=0.5'})

#Palabra de busqueda

#search_key = input('Ingresa el valor a buscar')
search_key ='casacas hombres'
search_key = search_key.replace(' ','+')
print(search_key)
base_url = 'https://www.amazon.com/s?k={}'.format(search_key)

items = []

#Buscar en las primeras 10 paginas
for i in range(10):
    print('Procesando {}...'.format(base_url + '&page={}'.format(i+1)))
    response = requests.get(base_url + '&page={}'.format(i+1), headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type' : 's-search-result'})
   

    for result in results:
        product_name = result.h2.text
        
        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find('span', {'class': 's-underline-text'}).text
          
            
        except  AttributeError:
            continue

        try:
            fecha = datetime.now()
            pagina =i+1
            
            tipo_moneda = result.find('span', {'class' : 'a-price-symbol'}).text
            prices1 = result.find('span', {'class' : 'a-price-whole'}).text
            prices2 = result.find('span', {'class' : 'a-price-fraction'}).text
            prices = float(prices1 + prices2)
            prices_original = result.find('span', {'class' : 'a-price a-text-price'}).find('span', {'aria-hidden':'true'}).text
            prices_original = float(prices_original[3::])
            descuento  =  1-prices/prices_original 
            product_url = 'https://amazon.com' + result.h2.a['href']
            items.append([search_key, fecha, pagina, product_name, rating, rating_count, tipo_moneda, prices, prices_original,descuento, product_url])
            

        except  AttributeError:
            continue
        sleep(1.5)
    print(i)
df = pd.DataFrame(items, columns = ['search_key', 'FechaExtract','Pages', 'NombreProducto', 'Rating', 'Rating_count','TipoMoneda', 'PrecioFinal', 'PrefioOriginal', 'Descuento', 'Url'])   
df.to_csv('{}.csv'. format(search_key), index = False, sep='\t')
    
        
