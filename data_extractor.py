from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

data_source = 'boursorama' # alphavantage or kaggle

if data_source == 'boursorama':

    file_root_path = "..\\Data\\Boursorama\\"
    file_share_path = "CASINOGUICPER_2018-12-29.txt"
    total_path = file_root_path+file_share_path
    df = pd.read_csv(total_path, delimiter=', ',
                     usecols=['date', 'ouv', 'haut', 'bas', 'clot', 'vol'])
    print('Loaded data from Boursorama')

    # Sort DataFrame by date
    df = df.sort_values('date')

    # Double check the result
    df.head()

    plt.figure(figsize = (18, 9))
    plt.plot(range(df.shape[0]), (df['bas']+df['haut'])/2.0)
    plt.xticks(range(0, df.shape[0], 500), df['date'].loc[::500], rotation=45)
    plt.xlabel('date', fontsize=18)
    plt.ylabel('Mid Price', fontsize=18)
    plt.show()

else :

    df = pd.read_csv(os.path.join('..\\Data\\Stocks','hpq.us.txt'),delimiter=',',usecols=['Date','Open','High','Low','Close'])
    print('Loaded data from the Kaggle repository')

    # Sort DataFrame by date
    df = df.sort_values('Date')

    # Double check the result
    df.head()

    plt.figure(figsize = (18,9))
    plt.plot(range(df.shape[0]),(df['Low']+df['High'])/2.0)
    plt.xticks(range(0,df.shape[0],500),df['Date'].loc[::500],rotation=45)
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Mid Price',fontsize=18)
    plt.show()
