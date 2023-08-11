from fastapi import FastAPI
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from pprint import pprint

app = FastAPI()

# cargamos los datos
movies = pd.read_csv('data/movies_3.csv',low_memory=False)
original_language = pd.read_csv('data/original_language.csv',low_memory=False)
collections = pd.read_csv('data/collections.csv',low_memory=False)
directors = pd.read_csv("data/directors.csv", sep=",")
production_countries = pd.read_csv("data/movies_production_countries.csv", sep=",")
movies_production_companies = pd.read_csv("data/movies_production_companies.csv", sep=",")


# 1. función peliculas_idioma

@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):

    idioma = idioma.lower().strip()
    respuesta = (original_language[original_language.original_language == idioma]).shape[0]

    return {'idioma':idioma, 'cantidad':respuesta}

# --------------------------------

# 2. función peliculas_duracion

@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion( pelicula: str ): 
    '''  Se ingresa una pelicula. Debe devolver la duracion y el año..
    '''
    pelicula = pelicula.title().strip()
    pelis = movies[['title','runtime','release_year']]
    mensaje = "La pelicula {} no se encuentra en la base de datos".format(pelicula)



    if (pelis['title']==pelicula).any():
        pelis = pelis[pelis['title']==pelicula]
        duracion = pelis['runtime'].tolist()
        anios = pelis['release_year'].tolist()

  
        data = {
            'titulo':pelicula,
            'anio': anios, 
            'duración': duracion}
        
    else:
        data = {mensaje}

    return data

# --------------------------------

# 3. función franquicia

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    franquicia = franquicia.title().strip()
    cantidad = collections[collections.name_collection == franquicia].shape[0]

    if cantidad == 0:
        out = {f'La franquicia "{franquicia}" no se encuentra en nuestra base de datos. Intente nuevamente.'}

    else:
        ganancia_total = int(collections.revenue[collections.name_collection == franquicia].sum())
        ganancia_promedio = ganancia_total/cantidad
        out = {'franquicia':franquicia, 'cantidad':cantidad, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}

    return out
