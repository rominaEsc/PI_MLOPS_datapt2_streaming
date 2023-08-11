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
    respuesta = (original_language.original_language ==idioma).shape[0]

    return {'idioma':idioma, 'cantidad':respuesta}
