#!/usr/bin/env python
# coding: utf-8

import pandas as pd

amazon_df = pd.read_parquet("./datasets/amazon_prime_titles.parquet")
disney_plus_df = pd.read_parquet("./datasets/disney_plus_titles.parquet")
netflix_title_df = pd.read_parquet("./datasets/netflix_titles.parquet")
hulu_df = pd.read_parquet("./datasets/hulu_titles.parquet")
rating_df = pd.read_parquet("./datasets/rating_total.parquet")
rating_df = rating_df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)


def generate_id(df, platform_name):
    """
    Genera un ID combinando la primera letra del nombre de la plataforma y el número de show_id

    Argumentos:
    df -- DataFrame de entrada
    platform_name -- str: nombre de la plataforma de streaming

    Devuelve:
    str -- ID generado
    """
    show_id = df["show_id"]
    return platform_name[0] + str(show_id)


def create_id_column(df, platform_name, generate_id_func):
    """
    Crea una columna 'movieId' en el DataFrame que contiene los IDs generados

    Argumentos:
    df -- DataFrame de entrada
    platform_name -- str: nombre de la plataforma de streaming
    generate_id_func -- función que genera el ID utilizando el DataFrame y el nombre de la plataforma

    Devuelve:
    df -- DataFrame con una columna 'movieId' que contiene los IDs generados
    """
    df["movieId"] = df.apply(generate_id_func, args=(platform_name,), axis=1)
    pop_id = df.pop("movieId")
    df.insert(0, "movieId", pop_id)
    df.drop(columns=["show_id"], inplace=True)


def cleaning_rows(df):
    """
    Limpia los valores de las celdas de un DataFrame eliminando los espacios en blanco y convirtiendo
    todos los caracteres a minúsculas.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame a limpiar.

    Returns:
    --------
    pandas.DataFrame
        DataFrame con los valores de las celdas limpios.
    """
    df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
    df = df.rename(columns={"rating": "classification"})
    return df


def fill_na(df):
    """
    Rellena valores NaN en la columna 'rating' con el valor 'G'

    Argumentos:
    df -- DataFrame de entrada

    Devuelve:
    df -- DataFrame con valores NaN en la columna 'rating' rellenados con 'G'
    """
    df["rating"].fillna(value="G", inplace=True)


def format_dates(df):
    """
    Formatea las fechas en el formato 'YYYY-MM-DD'

    Argumentos:
    df -- DataFrame de entrada

    Devuelve:
    df -- DataFrame con fechas formateadas en el formato 'YYYY-MM-DD'
    """
    df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
    df["date_added"] = pd.to_datetime(df["date_added"]).dt.strftime("%Y-%m-%d")
    return df


def duration_distrib(df):
    """
    Divide la columna 'duration' en dos columnas 'duration_int' y 'duration_type'

    Argumentos:
    df -- DataFrame de entrada

    Devuelve:
    df -- DataFrame con dos columnas adicionales 'duration_int' y 'duration_type'
    """

    df[["duration_int", "duration_type"]] = df["duration"].str.split(expand=True)
    df["duration_int"] = df["duration_int"].astype(float).astype("Int64")
    df.drop(columns="duration", inplace=True)
    return df


def main(df, platform_name):
    """
    Limpia y transforma un DataFrame dado utilizando las funciones cleaning_rows, create_id_column,
    fill_na, format_dates y duration_distrib.

    Argumentos:
    df -- DataFrame de entrada
    platform_name -- str: nombre de la plataforma de streaming

    Devuelve:
    DataFrame -- DataFrame con las transformaciones aplicadas.
    """

    create_id_column(df, platform_name, generate_id)
    fill_na(df)
    format_dates(df)
    duration_distrib(df)
    return cleaning_rows(df)


def data():
    list_df = [
        main(amazon_df, "amazon"),
        main(hulu_df, "hulu"),
        main(netflix_title_df, "netflix"),
        main(disney_plus_df, "disney"),
    ]
    list_df_merged = [
        pd.merge(df, rating_df, on="movieId", how="inner", sort=False) for df in list_df
    ]
    return dict(zip(["amazon_prime", "hulu", "netflix", "disney_plus"], list_df_merged))


if __name__ == "__main__":
    data()
