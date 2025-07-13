
from datetime import datetime, timedelta
import os
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from loguru import logger
import pandas as pd

logger.add("monitoramento.log")
app = FastAPI()
with open('modelo.pkl', 'rb') as f:
    model = pickle.load(f)

class InputData(BaseModel):
    days: int

@app.post("/predict")
def predict(data: InputData):
    last_date = datetime.strptime([x for x in os.listdir() if 'date.' in x][0].replace("date.",""),"%Y-%m-%d")
    new_ts = (datetime.now() + timedelta(days=data.days))
    offset =  (new_ts - datetime.now()).days
    periods = offset + (datetime.now() - last_date).days
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    result = forecast[['ds', 'yhat']][::-1][:offset]
    logger.info(f"dias de previsão {data.days} a partir de {datetime.now()}. Resultados:\n{result}")
    return {"resultado": result}