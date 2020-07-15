import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from stockstats import StockDataFrame as sdf

df=yf.download('TATASTEEL.NS', start='2020-07-09', end='2020-07-10', interval='5m')

df_copy=df.copy()

def vwap(df):
  df['Cum_Vol'] = df['Volume'].cumsum()
  df['Cum_Vol_Price'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close'] ) /3).cumsum()
  df['VWAP'] = df['Cum_Vol_Price'] / df['Cum_Vol']
  return df
  
nine_ema=df.Close.ewm(span=9,adjust=False).mean()

df_copy=vwap(df_copy)
df['VWAP']=df_copy['VWAP']
df['9EMA']=nine_ema

def buy_sell(signal):
  advice_list=[]
  global flag
  global mbuy
  for i in range(1,len(signal)):
    if signal['VWAP'][i] > signal['Close'][i] and signal['VWAP'][i-1] <= signal['Close'][i-1]:
      if flag != 1:
        advice_list.append('BUY '+'at '+ str(signal['Close'][i]))
        mbuy=signal['Close'][i]
        flag=1
    elif signal['VWAP'][i] < signal['Close'][i] and signal['VWAP'][i-1] >= signal['Close'][i-1]:
      if flag != 0:
        if mbuy<signal['Close'][i] and mbuy!=0:
          advice_list.append('SELL '+'at '+ str(signal['Close'][i]))
          flag=0
  return advice_list
mbuy=0
flag=-1
a = buy_sell(df)
#df['Buy_Signal_Price']=a[0]
#df['Sell_Signal_Price']=a[1]
print(a)
