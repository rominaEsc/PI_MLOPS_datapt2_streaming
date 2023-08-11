# PI_MLOPS_datapt2_streaming

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>
# <p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

<p align="center">

## Rol a desarrollar:
En este proyecto se nos propone, desarrollar el rol de un Data Scientist que comenzo a trabajar en una start-up que provee servicios de agregación de plataformas de streaming.  
 
## Objetivos:
Realizar un MVP que cumpla con las siguientes etapas:

# Requerimientos

A partir de los dataset que se encuentran en https://drive.google.com/drive/folders/1KSWEKuOyyQ_5INWQHApqwBSXgdQ1HkLg?usp=sharing


1- Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,poster_path y homepage. 

2- Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.

3- Los valores nulos del campo release date deben eliminarse.

4- Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.

5- De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.

6- Algunos campos, como belongs_to_collection, production_companies y otros (ver diccionario de datos) están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, ¡deberán desanidarlos y unirlos al dataset de nuevo para hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.. (ver 3_creacion_de_tablas.ipynb)


_<< Estas transformaciones y otras se realizaron los archivos: 1 a 4 >>_

Estos crean, en la carpeta data, los datasets a utilizar en este proyecto_ 

### Desarrollo API:
Debemos crear 6 funciones para los endpoints que se consumirán en la API.

- def peliculas_idioma( Idioma: str ): Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). Debe devolver la cantidad de películas producidas en ese idioma.
                    Ejemplo de retorno: X cantidad de películas fueron estrenadas en idioma

- def peliculas_duracion( Pelicula: str ): Se ingresa una pelicula. Debe devolver la duracion y el año.
                    Ejemplo de retorno: X . Duración: x. Año: xx

- def franquicia( Franquicia: str ): Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
                    Ejemplo de retorno: La franquicia X posee X peliculas, una ganancia total de x y una ganancia promedio de xx

- def peliculas_pais( Pais: str ): Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo.
                    Ejemplo de retorno: Se produjeron X películas en el país X

- def productoras_exitosas( Productora: str ): Se ingresa la productora, entregandote el revunue total y la cantidad de peliculas que realizo.
                    Ejemplo de retorno: La productora X ha tenido un revenue de x

- def get_director( nombre_director ): Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.



_<< Estas funciones se realizaron y probaron en el archivo 6>>_

### Deployment
Realizar el deployment para poder consumir la API

_<< Las consultas a la API pueden realizarse en el siguiente link: https://pi-mlops-datapt2-streaming.onrender.com/docs >>_

### Análisis exploratorio de los datos
Se realizo un analisis de las palabras que se presentaban con mayor frecuencia en el dataset. 
  
_<< Esto puede verse en el archivo 5 >>_


### Sistema de recomendación
El sistema consiste en recomendar películas a los usuarios basándose en películas similares, por lo que se debe encontrar la similitud de puntuación entre esa película y el resto de películas, se ordenarán según el score de similaridad y devolverá una lista de Python con 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente. Debe ser deployado como una función adicional de la API anterior y debe llamarse:
def recomendacion( titulo ): Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

_ver archivos 7 y 8_

## Video: 
Realizar un video mostrando el resultado de las consultas propuestas y de tu modelo de ML entrenado!

El video se encuentra en: https://drive.google.com/drive/folders/1q61TCXfbav8owsnG8ugasCN6GDkinTEm?usp=sharing