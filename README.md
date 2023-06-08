
# LAB01: MLOps

Este repositorio corresponde al primer proyecto individual con la tematica de MLOps Engineer; el proyecto consiste en tomar 4 datasets de diferentes plataformas de streaming y crear un MVP (Minimum Viable Product). El repositorio consistente en:

- API con 6 diferentes endpoints
- EDA notebook
- Deployment

## Herramientas utilizadas

**API:** FASTAPI, Uvicorn

**EDA:** Pandas, Numpy, Matplotlib, Seaborn, AutoViz

**Deployment:** Render

## Arquitectura de proyecto

```
--> api/
    - app.py

--> cleaning/
    - main_cleaning.py
    - EDA.ipynb

--> datasets/
    - amazon_prime_titles.parquet
    - hulu_titles.parquet
    - rating_total.parquet
    - disney_plus_titles.parquet
    - netflix_titles.parquet

- .gitattributes
- .gitignore
- requirements.txt
```

## API Reference

#### get_max_duration

```http
  GET /{platform}/get_max_duration?year={year}&duration_type={duration_type}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `platform` | `string` | **Required**. La plataforma de streaming deseada. |
| `year` | `int` | **Required**. El año de lanzamiento deseado de la película. |
| `duration_type` | `string` | **Required**. El tipo de duración deseada, solo puede ser 'min'. |

*Obtiene la película con la duración máxima para un año y plataforma específicos.*

#### get_score_count

```http
  GET /{platform}/get_score_count?scored={scored}&year={year}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `platform` | `string` | **Required**. La plataforma de streaming deseada. |
| `year` | `int` | **Required**. Año a considerar para el conteo de películas. |
| `scored` | `float` | **Required**. Puntaje mínimo para filtrar las películas |

*Cantidad de películas (sólo películas, no series, ni documentales, etc) según plataforma, con un puntaje mayor a XX en determinado año.*

### get_count_platform

```http
  GET /{platform}/get_count_platform
```

| Parameter  | Type      | Description                                         |
| :--------- | :--------| :---------------------------------------------------|
| `platform` | `string` | **Obligatorio**. La plataforma de streaming deseada.    |
| `year`     | `int`    | **Obligatorio**. Año a considerar para el conteo de películas. |
| `scored`   | `float`  | **Obligatorio**. Puntaje mínimo para filtrar las películas. |

*Obtiene el número total de películas disponibles en una plataforma de streaming.*

### get_actor

```http
  GET /{platform}/get_actor?year={year}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `platform` | `str` | **Obligatorio**. El nombre de la plataforma a buscar. |
| `year`     | `int` | **Obligatorio**. El año de lanzamiento a buscar.      |

*Devuelve el actor más común en una plataforma y año dado.*

### prod_per_country

```http
  GET /{platform}/prod_per_country?tipo={tipo}&pais={pais}&anio={anio}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `platform` | `str` | **Obligatorio**. El nombre de la plataforma a buscar.|
| `tipo`| `str` | **Obligatorio**.  El tipo de producción a buscar|
| `pais`| `str` | **Obligatorio**.  El país de origen a buscar|
| `anio`| `int` | **Obligatorio**. El año de lanzamiento a buscar|

*Retorna la cantidad de producciones de un determinado tipo en un país y año específicos.*

### get_contents

```http
    GET /{platform}/get_contents?rating={rating}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `platform` | `str` | **Obligatorio**. El nombre de la plataforma a buscar.|
| `rating`| `str` | **Obligatorio**.  Valor del rating de audiencia a filtrar (p.ej. "g", "pg", "r", etc.).|

*Retorna la cantidad total de contenidos/productos (todo lo disponible en streaming, series, películas, etc) según el rating de audiencia dado (para que público fue clasificada la pelicula).*

### predict

```http
    GET /{platform}/predict/{user_id}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `platform` | `str` | **Obligatorio**. El nombre de la plataforma a buscar.|
| `user_id`| `int` | **Obligatorio**.  El ID del usuario para el que se quieren hacer las recomendaciones.|

*Devuelve una lista con los títulos de las 5 películas más recomendadas para el usuario especificado.*

## Ejecutar API

Ejecutar el script de las APIs.

**Windows**

```bash
  python api/app.py
```

**MacOS y Linux**

```bash
python3 api/app.py
```

El servidor local de `uvicorn` es activado automaticamente al momento de ejecutar el script.

## EDA: Análisis Exploratorio de Datos

Con el análisis exploratorio de datos se busca encontrar todos esos Outliers o errores dentro de los diferentes Datasets dispuesto para resolver este proyecto; para esto fue dispuesto el archivo `cleaning/EDA.ipynb` donde se desarrollo este ejercicio de análisis y busqueda de datos.


## Deployment

No fue posible realizar el despliegue de la plataforma debido a la escasez de recursos de las plataformas y al alto consumo de recursos del presente proyecto. Sin embargo, el proyecto demostrará su funcionamiento en el video. 


## Video 

Link al video [aquí](https://www.youtube.com/watch?v=s0DsIfrSd90).
