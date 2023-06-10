from fastapi import FastAPI, status
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import HTTPException
import pandas as pd
import pickle
import datetime
import calendar


app = FastAPI()


# * Traer datasets necesarios

df = pd.read_parquet("datasets/movies_dataset.parquet")
short_df = pd.read_parquet("datasets/short_df.parquet")

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
        "Wednesday": "miércoles",
        "Thursday": "jueves",
        "Friday": "viernes",
        "Saturday": "sábado",
        "Sunday": "domingo",
    }

    if dia.lower() not in weekdays.values():
        return {"dia": dia, "cantidad": 0}

    movies_df["release_date"] = pd.to_datetime(movies_df["release_date"])

    movies_df["weekday"] = (
        movies_df["release_date"].dt.day_name(locale="es_ES").str.lower()
    )

    week_day = movies_df[movies_df["weekday"] == dia.lower()]

    return {"dia": dia, "cantidad": len(week_day)}
