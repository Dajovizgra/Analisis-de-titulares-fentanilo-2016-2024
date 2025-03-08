# -*- coding: utf-8 -*-
"""WebSscrapingAnálisisdeMediosMediaCloud.ipynb

**Importación de las librerias necesarias para la extración de la información.**
"""

!pip install mediacloud
import os, mediacloud.api
from importlib.metadata import version
import datetime as dt
from IPython.display import JSON
import requests
import pandas as pd
import csv
from google.colab import files
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

"""**Configuración del API Key de Media Cloud.**"""

MC_API_KEY = 'Your API Key'
search_api = mediacloud.api.SearchApi(MC_API_KEY)
f'Using Media Cloud python client v{version("mediacloud")}'

"""**Selecciones de las colecciones con las que cuenta Media Cloud y de donde se quiere extraer la información.**"""

COLLECTION_US_NATIONAL = 34412234
US_SPANISH_LANGUAGE_COLLECTION = 196136637
MEXICO_STATE_LOCAL = 38380322
MEXICO_NATIONAL = 34412427
COLOMBIA_STATE_LOCAL = 38379514
COLOMBIA_NATIONAL = 34412358


id_colections = [COLLECTION_US_NATIONAL, US_SPANISH_LANGUAGE_COLLECTION, MEXICO_NATIONAL, MEXICO_STATE_LOCAL, COLOMBIA_NATIONAL, COLOMBIA_STATE_LOCAL]

"""**Parámetros básicos de la solicitud.**

* En este punto, para hacer una busqueda en otro idioma, por ejemplo inglés, solo basta con usar colecciones en ese idioma.
"""

my_query = '"fentanilo"'
start_date = dt.date(2024, 1, 1)
end_date = dt.date(2024, 12, 31)

search_api.story_count(my_query, start_date, end_date, id_colections)

"""**Convertir las fechas a un formato ISO y serializar los resultados a un formato JSON.**"""

results = search_api.story_count_over_time(my_query, start_date, end_date, id_colections)

for item in results:
    if 'date' in item and isinstance(item['date'], dt.date):
        item['date'] = item['date'].isoformat()

JSON(results)

"""**Recuperar todos los resultados de la búsqueda, paginando a través de las páginas devueltas por la API.**"""

all_stories = []
more_stories = True
pagination_token = None
while more_stories:
    page, pagination_token = search_api.story_list(my_query, dt.date(2024,12,2), dt.date(2024,12,5), #Explicar los errores presentados cuando los resultados eran mayores de 2000, github.
                                                   id_colections,
                                                   pagination_token=pagination_token)
    all_stories += page
    more_stories = pagination_token is not None
len(all_stories)

"""**Escribir los resultados de la búsqueda en un archivo CSV llamado story-list.**"""

fieldnames = ['id', 'publish_date', 'title', 'url', 'language', 'media_name', 'media_url', 'indexed_date']

with open('story-list.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for s in all_stories:
        writer.writerow(s)

df = pd.read_csv('story-list.csv')
df.head()

"""**Los siguientes bloques cumplen con una función de limpieza pensando en un análisis mayor a futuro.**

* Las funciones cumplen con el objetivo de descartar aquellas urls que no den respuestas a las solicitudes o den algún error. Con esto se asegura de que más adelante, si se quiere obtener por ejemplo una captura de pantalla o información aparte de las columnas que están en el csv creado con los resultados, se podrá acceder a cualquier enlace porque todos deberían estar funcionando.

* La segunda función buscó que esta depuración de urls fuera más estable ya que la primera podía tardar más de 10 min ejecutando aún cuando se usaron archivos de prueba con solo 10 registros. De igual manera podía pasar que archivos con 200 registros fueran ejecutados en menos de 1 min.
"""

def eliminar_urls_no_validas(csv_file):
    # Cargar el csv en un DataFrame
    df = pd.read_csv('/content/Validacion.csv')
    urls_no_validas = []

    # Iterar sobre las URLs en la columna 'url'
    for index, row in df.iterrows():
        url = row['url']
        try:
            # Hacer una solicitud GET a la URL
            response = requests.get(url)
            # Si la respuesta es 404, agregar la URL a la lista de URLs no válidas
            if response.status_code == 404:
                urls_no_validas.append(url)
        except requests.exceptions.RequestException as e:
            # Si hay un error en la solicitud, agregar la URL a la lista de URLs no válidas
            urls_no_validas.append(url)

# Imprimir los dominios de las URLs no válidas
    dominios_no_validos = [urlparse(url).netloc for url in urls_no_validas]
    print("Dominios de URLs no válidas:")
    for dominio in dominios_no_validos:
        print(dominio)

    # Eliminar las filas con URLs no válidas del DataFrame
    df = df[~df['url'].isin(urls_no_validas)]

    # Guardar el DataFrame modificado en un nuevo csv
    df.to_csv('urls_validas.csv', index=False)

# Llamar a la función con el nombre del csv
eliminar_urls_no_validas('/content/Validacion.csv')

"""* En esta función se agrega un timeout por alguna solicitud tarda demasiado en responder, se cancela y se considerará como una URL no válida.
También se utiliza un pool de conexiones para hacer varias solicitudes al mismo tiempo y se utiliza una biblioteca de concurrencia para mejorar el rendimiento y reducir el tiempo de ejecución.
"""

def eliminar_urls_no_validas(csv_file):
    # Cargar el csv en un DataFrame
    df = pd.read_csv('/content/story-list.csv')
    urls_no_validas = []

    # Función para verificar una URL
    def verificar_url(url):
        try:
            # Hacer una solicitud GET a la URL con un timeout de 5 segundos
            response = requests.get(url, timeout=5)
            # Si la respuesta es 404, agregar la URL a la lista de URLs no válidas
            if response.status_code == 404:
                return url
        except requests.exceptions.RequestException:
            # Si hay un error en la solicitud, agregar la URL a la lista de URLs no válidas
            return url
        return None

    # Utilizar un pool de conexiones para verificar las URLs
    with ThreadPoolExecutor(max_workers=10) as executor:
        resultados = list(executor.map(verificar_url, df['url']))

    # Agregar las URLs no válidas a la lista
    urls_no_validas = [url for url in resultados if url is not None]

    # Imprimir los dominios de las URLs no válidas
    dominios_no_validos = [urlparse(url).netloc for url in urls_no_validas]
    print("Dominios de URLs no válidas:")
    for dominio in dominios_no_validos:
        print(dominio)

    # Eliminar las filas con URLs no válidas del DataFrame
    df = df[~df['url'].isin(urls_no_validas)]

    # Guardar el DataFrame modificado en un nuevo csv
    df.to_csv('urls_validas.csv', index=False)

# Llamar a la función con el nombre del csv
eliminar_urls_no_validas('/content/story-list.csv')
