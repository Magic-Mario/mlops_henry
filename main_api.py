from fastapi import FastAPI, status
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import HTTPException
import pandas as pd
import pickle
import datetime
import calendar


app = FastAPI()


# * Traer datasets necesarios

df = pd.read_parquet(r"datasets/movie_dataset.parquet")
short_df = pd.read_parquet(r"datasets/short_df.parquet")

with open("model/similarity_matrix.pickle", "rb") as f:
    model = pickle.load(f)


# * API's


@app.get("/cantidad_filmaciones_mes/{mes}", status_code=status.HTTP_200_OK)
def cantidad_filmaciones_mes(mes: str):
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

    movie_month = df.loc[df["release_date"].dt.month == months[mes.lower()]]

    return {"mes": mes, "cantidad": str(len(movie_month))}


@app.get("/cantidad_filmaciones_dia/{dia}", status_code=status.HTTP_200_OK)
def cantidad_filmaciones_dia(dia: str):
    weekdays = {
        "Monday": "lunes",
        "Tuesday": "martes",
        "Wednesday": "miercoles",
        "Thursday": "jueves",
        "Friday": "viernes",
        "Saturday": "sabado",
        "Sunday": "domingo",
    }

    if dia.lower() not in weekdays.values():
        return {"dia": dia, "cantidad": 0}

    df["release_date"] = pd.to_datetime(df["release_date"])

    df["weekday"] = (
        df["release_date"].dt.day_name(locale="es_ES").str.lower()
    )

    week_day = df[df["weekday"] == dia.lower()]

    return {"dia": dia, "cantidad": len(week_day)}


@app.get('/score_titulo/{titulo}', status_code=status.HTTP_200_OK)
def score_titulo(titulo: str):
    
    score_df = df[df['title'] == titulo].copy()
    
    if len(score_df) == 0:
        return {"message": "Película no encontrada"}
    
    movie = score_df.iloc[0]

    response = f"La pelicula {movie['title']}"
    response += f" fue estrenada en el año {movie['release_year']}"
    response += f" con un score de {movie['popularity']}"
    
    return {"message": response}



@app.get('/voto_titulo/{titulo}', status_code=status.HTTP_200_OK)
def votos_titulo(titulo: str):
    vote_df = df.query("vote_count >= 2000").copy()
    movie = vote_df[vote_df['title'] == titulo].copy()
    
    if len(movie) == 0:
        return {"message": "Película no encontrada"}
    
    movie = movie.iloc[0]
    
    response = f"La película '{movie['title']}' fue estrenada en el año {movie['release_year']}."
    response += f" La misma cuenta con un total de {movie['vote_count']} valoraciones,"
    response += f" con un promedio de {movie['vote_average']}."
    
    return {"message": response}



@app.get('/get_actor/{nombre_actor}', status_code=status.HTTP_200_OK)
def get_actor(nombre_actor: str):
    pass 