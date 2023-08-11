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

# --------------------------------

# 4. función peliculas_pais

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    pais = pais.upper()
    cantidad =  int(production_countries.id_production_countries[production_countries.id_production_countries == pais].count())
    
    return {'pais':pais, 'cantidad':cantidad}

# --------------------------------

# 5. función productoras_exitosas

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    productora = productora.title().strip()

    df = movies_production_companies[movies_production_companies.name_production_companies == productora]

    revenue_total = int(df.revenue.sum())
    cantidad = int(df.revenue.count())

    return {'productora':productora, 'revenue_total': revenue_total,'cantidad':cantidad}

# --------------------------------

# 6. funcion get_director

@app.get('/get_director/{nombre_director}')
def get_director( nombre_director ): 
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    A demás, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
       
    nombre_director = nombre_director.title().strip()
    
    existe = directors[directors.name == nombre_director].shape[0]

    if existe == 0:
        data = {f'No se encontraron directores con el nombre {nombre_director}.'}

    else:
   
        id_director = directors[directors.name == nombre_director].iloc[0,0]

        df = (
            pd.merge(
                directors[directors['id_director'] == id_director],
                movies[['id_movie','title','release_year','revenue','budget','return']],
                on='id_movie', 
                how='inner')
        )
        
        retorno_total_director = df['return'].sum()
        peliculas = df['title'].tolist()
        anios = df['release_year'].tolist()
        retorno_peliculas = df['return'].tolist()
        budget_peliculas = df['budget'].tolist()
        revenue_peliculas = df['revenue'].tolist()

        data = {
            'director':nombre_director, 
            'retorno_total_director':retorno_total_director, 
            'peliculas':peliculas, 
            'anio':anios, 
            'retorno_pelicula':retorno_peliculas, 
            'budget_pelicula':budget_peliculas, 
            'revenue_pelicula':revenue_peliculas}

    return data


#  -----------------------------


# ML

# Instanciamos el CV
vectorizer = CountVectorizer()
stopwords = STOPWORDS
# eliminamos las "stop words", palabras comunes no informativas
tf = TfidfVectorizer(stop_words='english')

# calculamos los features para cada ítem (texto)
tfidf_matrix = tf.fit_transform(df['text'])

# calculamos las similitudes entre todos los documentos
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
n = 5

results = {} 
for idx, row in df.iterrows():
    # guardamos los indices similares basados en la similitud coseno. Los ordenamos en modo ascendente, siendo 0 nada de similitud y 1 total
    similar_indices = cosine_similarities[idx].argsort()[:-n-2:-1] 
    # guardamos los N más cercanos
    similar_items = [(f"{df.loc[i, 'title']}") for i in similar_indices]
    results[f"{row['title']}"] = similar_items[1:]


@app.get('/recomendacion/{titulo}')

def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    titulo = titulo.title().strip()

    if df['title'].str.contains(titulo).any():
        titulo = titulo.title().strip()
        lista = (results[titulo])
        data = {'titulo':titulo , 'lista recomendada': lista}
    else:
        mensaje = "La pelicula {} no se encuentra en la base de datos.".format(titulo)
        data = {'actor':[mensaje] }    
    return data