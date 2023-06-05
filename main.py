from fastapi import FastAPI
import pandas as pd

#instanciamos la api
app = FastAPI()


#leemos la tabla
data = pd.read_csv('data/peliculas_ETL.csv')
df = data.copy()

# para la funcion 1 y 2, debo aplicar esta modificacion.
#  comentare cada una con respecto a la funcion que corresponden
df['release_date'] = pd.to_datetime(df['release_date'])


#funcion3:
#aplicamos un trim para eliminar espacios
df['title'] = df['title'].str.strip()


#Damos la bienvenida en nuestro root
@app.get('/')
async def inicio():
    return 'Bienvenidos a esta api de peliculas, comienza la aventura!'



#Funcion 1: Cantidad de films estrenados por mes.
@app.get('/films_mes')
async def cantidad_filmacion_mes(mes: str = None):
    """
    Devuelve la cantidad de films estrenados en un mes.

    parametros
    ---------
    mes: un string con el nombre del mes en español, ej: enero
    """
    #evitamos errores con lower()
    mes = mes.lower()
    #creamos una lista con los meses en minuscula
    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    #si el mes no se encuentra en la lista devuelve un ejemplo
    if mes not in meses:
        return "ingresa el nombre de un mes en español. Ej: Agosto"
    #si existe tomamos el indice del mes.
    indice_mes = meses.index(mes)
    #de nuestro df recuperamos en orden los valores de las peliculas que se estrenaron en cada mes.
    valores_mes = list(df.release_date.dt.month.value_counts().sort_index())
    return (f"En el mes de {mes.title()}, se estrenaron {valores_mes[indice_mes]} peliculas!")




#Funcion 2. Cantidad de films estrenados por dia de la semana
@app.get('/films_dia')
async def cantidad_filmaciones_dia(dia: str = None):
    """
    Devuelve la cantidad de films estrenados en dias de la semana

    parametros
    -----------
    dia: nombre del dia de la semana en español. ej: lunes
    """
    #minimizamos errores.
    dia = dia.lower()
    #lista con los dias de la semana en minuscula
    semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    #chequeamos si el dia se encuentra en nuestra semana.
    if dia not in semana:
        return "ingresa el nombre del dia en español. ej: Lunes"
    #recuperamos el indice
    indice_semana = semana.index(dia)
    #lista con cantidades de pelicula por dia.
    valores_semana = list(df.release_date.dt.weekday.value_counts().sort_index())
    return (f"En el dia {dia.title()}, se han estrenado {valores_semana[indice_semana]} peliculas!")
    

#Funcion 3. Devolver un titulo con el anio de estreno y el score
@app.get('/score_titulo')
async def score_titulo(titulo: str = None):
    """
    Devuelve titulo, anio de estreno y score de una 
    pelicula de nuestra base de datos.

    parametros
    ----------
    titulo: titulo de la pelicula completo.
    """
    #input a minusculas para evitar errores
    titulo = titulo.lower()
    #hacemos un try except, si pasa se completa la funcion
    try:
        #creamos una mascara para la pelicula
        mask = df[df['title'].str.lower()  == titulo]
        #extraemos valores y damos respuesta.
        anio = mask['release_year'].values[0]
        score = mask['vote_average'].values[0]
        return (f'La pelicula {titulo.title()}, se lanzo en el año {anio}, y tiene una puntuacion de {score}.')
    except:
        #si no pasa se pide otra pelicula
        return 'Ingresa por favor el nombre de la pelicula. ej: Toy Story'
    
    