from fastapi import FastAPI, status
from fastapi.responses import Response, JSONResponse
from fastapi.exceptions import HTTPException
import pandas as pd
app = FastAPI()


#* Traer datasets necesarios

df = pd.read_parquet('datasets/movies_dataset.parquet')
short_df = pd.read_parquet('datasets/short_df.parquet')