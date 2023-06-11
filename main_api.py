from fastapi import FastAPI, status
import pandas as pd
import numpy as np
import pickle
import datetime
import calendar


app = FastAPI()


# * Traer datasets necesarios

df = pd.read_parquet(r"datasets/movie_dataset.parquet")
merged_df = pd.read_parquet(r"datasets/merged_df.parquet")
short_df = pd.read_parquet(r"datasets/short_df.parquet")

with open("model/similarity_matrix.pickle", "rb") as f:
    model = pickle.load(f)


# * API's


@app.get("/cantidad_filmaciones_mes/{mes}", status_code=status.HTTP_200_OK)
def cantidad_filmaciones_mes(mes: str):
    """
    Obtiene la cantidad de filmaciones de películas en un mes específico.

    Args:
        mes (str): Nombre del mes en español.

    Returns:
        dict: Diccionario con el nombre del mes y la cantidad de filmaciones de películas en ese mes, o un mensaje de error si el nombre del mes no es válido.
    """
    # Diccionario de meses en español y su correspondiente número de mes
    months = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12,
    }

    # Verificar si el nombre del mes proporcionado es válido
    if mes.lower() not in months:
        return {"message": f"Nombre de mes inválido: {mes}"}

    # Filtrar las filas por el mes proporcionado
    movie_month = df.loc[df["release_date"].dt.month == months[mes.lower()]]

    # Construir la respuesta con el nombre del mes y la cantidad de filmaciones
    return {"mes": mes, "cantidad": str(len(movie_month))}


@app.get("/cantidad_filmaciones_dia/{dia}", status_code=status.HTTP_200_OK)
def cantidad_filmaciones_dia(dia: str):
    """
    Obtiene la cantidad de filmaciones de películas en un día específico.

    Args:
        dia (str): Nombre del día de la semana en inglés.

    Returns:
        dict: Diccionario con el nombre del día y la cantidad de filmaciones de películas en ese día, o 0 si el nombre del día no es válido.
    """
    # Diccionario de días de la semana en inglés y español
    weekdays = {
        "Monday": "lunes",
        "Tuesday": "martes",
        "Wednesday": "miércoles",
        "Thursday": "jueves",
        "Friday": "viernes",
        "Saturday": "sábado",
        "Sunday": "domingo",
    }

    # Verificar si el nombre del día proporcionado es válido
    if dia.title() not in weekdays:
        return {"dia": dia, "cantidad": 0}

    # Convertir la columna "release_date" a tipo datetime
    df["release_date"] = pd.to_datetime(df["release_date"])

    # Agregar una columna "weekday" con el nombre del día de la semana en español
    df["weekday"] = df["release_date"].dt.day_name(locale="es_ES").str.lower()

    # Filtrar las filas por el día de la semana proporcionado
    week_day = df[df["weekday"] == weekdays[dia.title()]]

    return {"dia": weekdays[dia.title()], "cantidad": len(week_day)}



@app.get("/voto_titulo/{titulo}", status_code=status.HTTP_200_OK)
def votos_titulo(titulo: str):
    """
    Obtiene información sobre el número de votos y el promedio de votos de una película específica.

    Args:
        titulo (str): Título de la película a consultar.

    Returns:
        dict: Diccionario con la información de la película o un mensaje de error si no se encuentra la película.
    """
    # Filtrar las películas con un mínimo de 2000 votos
    vote_df = df.query("vote_count >= 2000").copy()

    # Buscar la película por título
    movie = vote_df[vote_df["title"] == titulo].copy()

    # Verificar si la película fue encontrada
    if len(movie) == 0:
        return {"message": "Película no encontrada"}

    # Obtener la información de la primera película encontrada (asumiendo títulos únicos)
    movie = movie.iloc[0]

    # Construir la respuesta con la información de la película
    response = f"La película '{movie['title']}' fue estrenada en el año {movie['release_year']}."
    response += f" La misma cuenta con un total de {movie['vote_count']} valoraciones,"
    response += f" con un promedio de {movie['vote_average']}."

    return {"message": response}


@app.get("/get_actor/{nombre_actor}", status_code=status.HTTP_200_OK)
def get_actor(nombre_actor: str):
    """
    Obtiene información sobre un actor específico, incluyendo el número de películas en las que ha participado,
    el retorno total obtenido y el promedio de retorno.

    Args:
        nombre_actor (str): Nombre del actor a consultar.

    Returns:
        str: Cadena de texto con la información del actor y sus películas.
    """
    # Filtrar las filas que contengan al actor en la lista de actores
    actor_rows = merged_df[merged_df["cast"].apply(lambda cast: nombre_actor in cast)]

    num_pelis = len(actor_rows)
    retorno_total = actor_rows["return"].sum()
    retorno_promedio = actor_rows["return"].mean()

    response = f"El actor {nombre_actor} ha participado en {num_pelis} películas."
    response += f" Su retorno total es de {retorno_total} con un promedio de retorno de {retorno_promedio}."

    return response


@app.get("/get_director/{nombre_director}", status_code=status.HTTP_200_OK)
def get_director(nombre_director):
    """
    Obtiene información sobre un director específico, incluyendo su éxito promedio y detalles de sus películas.

    Args:
        nombre_director (str): Nombre del director a consultar.

    Returns:
        dict: Diccionario que contiene el nombre del director, el éxito promedio y una lista de películas con sus detalles.
    """
    # Filtrar las filas que contengan al director en la columna "director"
    director_rows = merged_df[
        merged_df["crew"].apply(lambda director: nombre_director in director)
    ]

    # Filtrar los valores infinitos de retorno
    director_returns = director_rows["return"]
    filtered_returns = director_returns[np.isfinite(director_returns)]

    # Calcular el éxito del director como el promedio de los valores de retorno
    exito = filtered_returns.mean()

    # Obtener información detallada de cada película del director
    peliculas = []
    for index, row in director_rows.iterrows():
        if np.isfinite(row["return"]):
            pelicula = {
                "titulo": row["title"],
                "fecha_lanzamiento": row["release_date"],
                "retorno_individual": row["return"],
                "costo": row["budget"],
                "ganancia": row["revenue"],
            }
            peliculas.append(pelicula)

    # Devolver los resultados
    return {"nombre_director": nombre_director, "exito": exito, "peliculas": peliculas}


@app.get("/recomendacion/{titulo}", status_code=status.HTTP_200_OK)
def recomendacion(titulo: str):
    """
    Obtiene recomendaciones de películas similares basadas en el título de una película dada.

    Parámetros:
    - titulo (str): El título de la película.

    Retorna:
    - List[str]: Una lista de títulos de películas recomendadas similares.
    """
    # Buscar la fila correspondiente al título de la película
    idx = short_df.index[short_df["title"].str.lower() == titulo.lower()].tolist()
    if len(idx) == 0:
        return "Película no encontrada"
    else:
        idx = idx[0]

    # Calcular la similitud de la película con todas las demás películas
    sim_scores = list(enumerate(model[idx]))

    # Ordenar las películas según su similitud y seleccionar las 5 más similares
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]

    # Obtener los índices de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]

    # Devolver los títulos de las películas recomendadas
    return list(short_df["title"].iloc[movie_indices])
