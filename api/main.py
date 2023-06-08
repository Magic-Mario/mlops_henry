from fastapi import FastAPI, status
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import HTTPException

# * Mis imports
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cleaning.main_cleaning import data


data_ = data()

app = FastAPI()
"""
Película (sólo película, no serie, ni documentales, etc) con mayor duración según año, plataforma y tipo de duración.
La función debe llamarse get_max_duration(year, platform, duration_type)
y debe devolver sólo el string del nombre de la película.
"""


@app.get("/{platform}/get_max_duration", status_code=status.HTTP_200_OK)
def get_max_duration(year: int, platform: str, duration_type: str) -> Response:
    """
    Obtiene la película con la duración máxima para un año y plataforma específicos.

    Args:
        year (int): El año de lanzamiento deseado de la película.
        platform (str): La plataforma de transmisión deseada.
        duration_type (str): El tipo de duración deseada, solo puede ser 'min'.

    Returns:
        Una respuesta HTTP que contiene el título de la película con la duración máxima.

    Raises:
        HTTPException: Si la plataforma o el año especificados no existen en los datos,
            o si no hay películas disponibles que cumplan con los criterios de búsqueda.
    """
    if platform not in data_:
        raise HTTPException(status_code=404, detail="Platform not found")
    platform = data_[platform]
    # Primero seleccionar sola las peliculas
    platform = platform[platform["type"] == "movie"]
    # Verificar si hay películas que cumplan con los criterios de búsqueda
    if platform[platform["release_year"] == year].empty:
        raise HTTPException(status_code=404, detail="No movies found for this year")
    if platform[platform["duration_type"] == duration_type].empty:
        raise HTTPException(
            status_code=404,
            detail="No movies available (Only recieve 'min' as argument)",
        )
    result = (
        platform[platform["release_year"] == year]
        .sort_values(by="duration_int", ascending=False)
        .iloc[0]["title"]
    )
    return Response(result)


""" 
Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma,
con un puntaje mayor a XX en determinado año. La función debe llamarse get_score_count(platform, scored, year)
y debe devolver un int, con el total de películas que cumplen lo solicitado.
"""


@app.get("/{platform}/get_score_count", status_code=status.HTTP_200_OK)
def get_score_count(platform: str, scored: float, year: int) -> int:
    """
    Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma,
    con un puntaje mayor a XX en determinado año.

    Args:
        platform (str): Plataforma de streaming (amazon_prime, hulu, netflix, disney_plus)
        scored (float): Puntaje mínimo para filtrar las películas
        year (int): Año a considerar para el conteo de películas

    Returns:
        int: Cantidad de películas que cumplen los criterios de búsqueda

    Raises:
        HTTPException(404): Si la plataforma no se encuentra en la base de datos
        HTTPException(404): Si no hay películas disponibles que cumplan con los criterios de búsqueda
    """
    if platform not in data_:
        raise HTTPException(status_code=404, detail="Platform not found")
    # Obtener solo las películas de la plataforma
    platform = data_[platform][data_[platform]["type"] == "movie"]

    # Filtrar por año y puntaje mínimo
    if (
        platform[platform["release_year"] == year].empty
        or platform[platform["rating"] >= scored].empty
    ):
        raise HTTPException(
            status_code=404, detail="No movies found for this year o with this score"
        )
    filtered = platform[
        (platform["release_year"] == year) & (platform["rating"] >= scored)
    ]
    # Verificar si hay películas que cumplan con los criterios de búsqueda
    if filtered.empty:
        raise HTTPException(
            status_code=404, detail="No movies found for this year and score"
        )
    # Devolver el conteo de películas
    return len(filtered)


"""
Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma.
La función debe llamarse get_count_platform(platform) y debe devolver un int,
con el número total de películas de esa plataforma.
Las plataformas deben llamarse amazon, netflix, hulu, disney.
"""


@app.get("/{platform}/get_count_platform", status_code=status.HTTP_200_OK)
def get_count_platform(platform: str) -> int:
    """
    Obtiene el número total de películas disponibles en una plataforma de streaming.

    Args:
        platform (str): El nombre de la plataforma de streaming a consultar. Debe ser uno de los nombres disponibles en el dataset.

    Returns:
        int: El número total de películas disponibles en la plataforma especificada.

    Raises:
        HTTPException: Si el nombre de la plataforma no es válido (no se encuentra en el dataset).
    """
    if platform not in data_:
        raise HTTPException(status_code=404, detail="Platform not found")
    # Obtener solo las películas de la plataforma
    platform = data_[platform][data_[platform]["type"] == "movie"]

    return platform.shape[0]


"""
Actor que más se repite según plataforma y año. La función debe llamarse get_actor(platform, year)
y debe devolver sólo el string con el nombre del actor que más se repite según la plataforma y el año dado.
"""


@app.get("/{platform}/get_actor", status_code=status.HTTP_200_OK)
def get_actor(platform: str, year: int) -> str:
    """
    Devuelve el actor más común en una plataforma y año dados.

    Args:
        platform (str): El nombre de la plataforma a buscar.
        year (int): El año de lanzamiento a buscar.

    Returns:
        str: El nombre del actor más común en la plataforma y año dados.

    Raises:
        HTTPException: Si la plataforma especificada no se encuentra o no hay actores disponibles.
    """
    if platform not in data_:
        raise HTTPException(status_code=404, detail="Platform not found")
    platform_data = data_[platform]
    platform_year_data = platform_data[platform_data["release_year"] == year]
    if platform_year_data.empty:
        raise HTTPException(
            status_code=404, detail="No data available for the specified year."
        )
    try:
        actors = platform_year_data["cast"].str.split(", ")
        actors_exploded = actors.explode()
        if actors_exploded.empty:
            raise AttributeError
        return actors_exploded.value_counts().index[0]
    except AttributeError as e:
        raise HTTPException(status_code=404, detail="No actor available") from e


""" 
La cantidad de contenidos/productos (todo lo disponible en streaming) que se publicó por país y año.
La función debe llamarse prod_per_county(tipo,pais,anio) deberia devolver la cantidada de contenidos/productos
segun el tipo de contenido (pelicula,serie) por pais y año en un diccionario
con las variables llamadas 'pais' (nombre del pais), 'anio' (año),
'pelicula' (cantidad de contenidos/productos).
"""


@app.get("/{platform}/prod_per_country", status_code=status.HTTP_200_OK)
def prod_per_country(platform: str, tipo: str, pais: str, anio: int):
    """
    Retorna la cantidad de producciones de un determinado tipo en un país y año específicos.

    Args:
        platform (str): La plataforma de streaming a buscar.
        tipo (str): El tipo de producción a buscar.
        pais (str): El país de origen a buscar.
        anio (int): El año de lanzamiento a buscar.

    Returns:
        dict: Un diccionario con las cantidades de producciones de acuerdo a los filtros aplicados.

    Raises:
        HTTPException: Si no se encuentra la plataforma de streaming en los datos.
        HTTPException: Si no se encuentra ningún registro con los filtros aplicados.
    """
    # Verificar que la plataforma de streaming exista en los datos
    if platform not in data_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La plataforma de streaming no existe en los datos",
        )

    # Filtrar los datos de la plataforma de streaming según los criterios de búsqueda
    platform_data = data_[platform]
    platform_filtered = platform_data.query(
        "type == @tipo and release_year == @anio and country == @pais"
    )

    # Verificar que se haya encontrado al menos un registro con los criterios de búsqueda
    if len(platform_filtered) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron registros con los criterios de búsqueda aplicados",
        )

    # Retornar un diccionario con la cantidad de producciones según los criterios de búsqueda
    return {"pais": pais, "anio": anio, "cantidad": len(platform_filtered)}


""" 
La cantidad total de contenidos/productos (todo lo disponible en streaming, series, peliculas, etc)
según el rating de audiencia dado (para que publico fue clasificada la pelicula).
La función debe llamarse get_contents(rating)
y debe devolver el numero total de contenido con ese rating de audiencias.
"""


@app.get("/{platform}/get_contents", status_code=status.HTTP_200_OK)
def get_contents(platform: str, rating: str) -> int:
    """
    Retorna la cantidad total de contenidos/productos (todo lo disponible en streaming, series, películas, etc)
    según el rating de audiencia dado (para que público fue clasificada la pelicula).

    Args:
        platform (str): Nombre de la plataforma de streaming (p.ej. Netflix, Amazon Prime, etc.).
        rating (str): Valor del rating de audiencia a filtrar (p.ej. "g", "pg", "r", etc.).

    Returns:
        int: Cantidad total de contenidos con el rating de audiencia dado.

    Raises:
        HTTPException: Si la plataforma especificada no se encuentra en los datos.
        HTTPException: Si el rating especificado no es válido.
    """

    # Verificar que la plataforma dada se encuentre en los datos
    if platform not in data_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La plataforma {platform} no se encuentra en los datos.",
        )

    platform_data = data_[platform]

    # Verificar que el rating dado sea válido
    if rating not in platform_data["classification"].unique():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El rating {rating} no es válido para la plataforma {platform}.",
        )

    platform_filtered = platform_data.query("classification == @rating")

    return len(platform_filtered)


from surprise import Dataset, Reader
from surprise import KNNWithMeans

@app.get("/{platform}/predict/{user_id}", status_code=status.HTTP_200_OK)
async def predict(platform: str, user_id: int):
    """
    Devuelve una lista con los títulos de las 5 películas más recomendadas para el usuario especificado.

    Args:
        platform (str): La plataforma de la que se quieren hacer las recomendaciones.
        user_id (int): El ID del usuario para el que se quieren hacer las recomendaciones.

    Returns:
        List[str]: Una lista con los títulos de las 5 películas más recomendadas.
    """

    platform_data = data_[platform]
    platform_data = platform_data.loc[:5000, :]
    
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(platform_data[["userId", "title", "rating"]], reader)
    trainset = data.build_full_trainset()
    algo = KNNWithMeans(k=50, sim_options={"name": "cosine", "user_based": True})
    algo.fit(trainset)
    # Obtiene las películas que el usuario aún no ha visto
    movies_watched = set(
        platform_data[platform_data["userId"] == user_id]["title"].unique()
    )
    movies_not_watched = list(set(platform_data["title"].unique()) - movies_watched)
    
    # Obtiene las predicciones de rating para las películas no vistas por el usuario
    testset = [[user_id, movie, 0] for movie in movies_not_watched]
    predictions = algo.test(testset)
    # Ordena las películas recomendadas según el rating predicho más alto
    top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:5]

    # Devuelve los títulos de las películas recomendadas
    return [prediction.iid for prediction in top_n]

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

