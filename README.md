
# LAB01: MLOps

Este repositorio corresponde al primer proyecto individual con la tematica de MLOps Engineer; el proyecto consiste en tomar 2 datasets correspondientes a creaciones cinematograficas y crear un MVP (Minimum Viable Product). El repositorio consistente en:

- API con 7 diferentes endpoints
- EDA notebook
- Deployment

## Herramientas utilizadas

**API:** FASTAPI, Uvicorn

**EDA:** Pandas, Numpy, Matplotlib, Seaborn

**Deployment:** Render

## Arquitectura de proyecto

```
--> datasets/
    - credits.parquet
    - merged_df.parquet
    - movies_dataset.parquet
    - short_df.parquet

--> model/
    - similarity_matrix.pickle

--> notebooks/
    - ex_da_an.ipynb
    - recommendation_model.ipynb
    - transformation.ipynb

- .gitignore
- .start.sh.swp
- main_api.py
- requirements.txt
```

## API Reference

#### cantidad_filmaciones_mes

```http
  GET /cantidad_filmaciones_mes/{mes}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `mes` | `str` | **Required**. Nombre del mes en español. |

*Obtiene la cantidad de filmaciones de películas en un mes específico.*

#### cantidad_filmaciones_dia

```http
  GET /cantidad_filmaciones_dia/{dia}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `dia` | `string` | **Required**. Nombre del día de la semana en inglés. |

- Obtiene la cantidad de filmaciones de películas en un día específico.*

### score_titulo

```http
  GET /score_titulo/{titulo}
```

| Parameter  | Type      | Description                                         |
| :--------- | :--------| :---------------------------------------------------|
| `titulo` | `string` | **Obligatorio**. Título de la película a consultar.|

*Obtiene el puntaje de popularidad de una película específica.*

### voto_titulo

```http
  GET /voto_titulo/{titulo}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `titulo` | `str` | **Obligatorio**. Título de la película a consultar. |

*Obtiene información sobre el número de votos y el promedio de votos de una película específica.*

### get_actor

```http
  GET /get_actor/{nombre_actor}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `nombre_actor` | `str` | **Obligatorio**.Nombre del actor a consultar.|

*Obtiene información sobre un actor específico, incluyendo el número de películas en las que ha participado, el retorno total obtenido y el promedio de retorno.*

### get_director

```http
    GET /get_director/{nombre_director}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `nombre_director` | `str` | **Obligatorio**. Nombre del director a consultar.|

*Obtiene información sobre un director específico, incluyendo su éxito promedio y detalles de sus películas.*

### recomendacion

```http
    GET /recomendacion/{titulo}
```

| Parámetro | Tipo   | Descripción                                         |
| :------- | :----- | :---------------------------------------------------|
| `titulo` | `str` | **Obligatorio**.  El título de la película.|

*Obtiene recomendaciones de películas similares basadas en el título de una película dada.*

## EDA: Análisis Exploratorio de Datos

Con el análisis exploratorio de datos se busca encontrar todos esos Outliers o errores dentro de los diferentes Datasets dispuesto para resolver este proyecto; para esto fue dispuesto el archivo `notebooks/ex_da_an.ipynb` donde se desarrollo este ejercicio de análisis y busqueda de datos.

## Deployment

El deployment fue realizado en la plataforma de Render y esta disponible para recibir consultas en el siguiente [link](https://magicmlops01.onrender.com/)

## Video

Link al video [aquí]().
