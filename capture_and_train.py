from prophet import Prophet
import yfinance as yf
import pandas as pd
from sklearn.metrics import *
import pickle

empresa = 'PETR4.SA'
data_inicial = '2025-01-01'
data_final = '2025-06-30'
df = yf.download(empresa, start=data_inicial, end=data_final)
df.columns = df.columns.get_level_values(0)

df.reset_index(inplace=True)  
df_new = df[['Date', 'Close']]
last_date = str(df_new[['Date']].max()['Date'].date())
with open(f"date.{last_date}","w"):
    ...
print(df_new.to_csv('dados.csv',index=False))
df = pd.read_csv('dados.csv')
df = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

model = Prophet()
model.fit(df)

with open("modelo.pkl","wb") as f:
    pickle.dump(model,f)


future = model.make_future_dataframe(periods=120)
forecast = model.predict(future)

actual = df['y'][-120:]
predicted = forecast['yhat'][-120:]

mse = mean_squared_error(actual, predicted)
mae = mean_absolute_error(actual, predicted)
mape = mean_absolute_percentage_error(actual,predicted)
print(f'MSE: {mse}')
print(f'MSE: {mae}')
print(f'MAPE: {mape}')