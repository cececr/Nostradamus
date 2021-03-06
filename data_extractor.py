from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

data_source = 'boursorama' # boursorama or kaggle

if data_source == 'kaggle':

    file_root_path = "..\\Data\\Boursorama\\"
    file_share_path = "CASINOGUICPER_2019-01-01.txt"
    total_path = file_root_path+file_share_path
    df = pd.read_csv(total_path, delimiter=', ',
                     usecols=['date', 'ouv', 'haut', 'bas', 'clot', 'vol'])
    print('Loaded data from Boursorama')

    # Sort DataFrame by date
    #df = df.sort_values('date')

    # Double check the result
    df.head()

    plt.figure(figsize = (18, 9))
    plt.plot(range(df.shape[0]), (df['bas']+df['haut'])/2.0)
    plt.xticks(range(0, df.shape[0], 500), df['date'].loc[::500], rotation=45)
    plt.xlabel('date', fontsize=18)
    plt.ylabel('Mid Price', fontsize=18)
    plt.show()

    plt.figure(figsize=(18, 9))
    plt.plot(range(df.shape[0]), (df['bas'] + df['haut']) / 2.0)
    # plt.plot(range(df.shape[0]), df['bas'])
    plt.xticks(range(0, df.shape[0], 500), df['date'].loc[::500], rotation=45)
    plt.xlabel('date', fontsize=18)
    plt.ylabel('Mid Price', fontsize=18)
    # plt.show()

    # First calculate the mid prices from the highest and lowest
    high_prices = df.loc[:, 'haut'].as_matrix()
    low_prices = df.loc[:, 'bas'].as_matrix()
    mid_prices = (high_prices + low_prices) / 2.0

    thresh_train_test = 3500
    train_data = mid_prices[:thresh_train_test]
    test_data = mid_prices[thresh_train_test:]

    # Scale the data to be between 0 and 1
    # When scaling remember! You normalize both test and train data with respect to training data
    # Because you are not supposed to have access to test data
    scaler = MinMaxScaler()
    train_data = train_data.reshape(-1, 1)
    test_data = test_data.reshape(-1, 1)

    smoothing_window_size = 500
    for di in range(0, 3000, smoothing_window_size):
        scaler.fit(train_data[di:di + smoothing_window_size, :])
        train_data[di:di + smoothing_window_size, :] = scaler.transform(train_data[di:di + smoothing_window_size, :])

    # You normalize the last bit of remaining data
    scaler.fit(train_data[di + smoothing_window_size:, :])
    train_data[di + smoothing_window_size:, :] = scaler.transform(train_data[di + smoothing_window_size:, :])

    # Reshape both train and test data
    train_data = train_data.reshape(-1)

    # Normalize test data
    test_data = scaler.transform(test_data).reshape(-1)

    # Now perform exponential moving average smoothing
    # So the data will have a smoother curve than the original ragged data
    EMA = 0.0
    gamma = 0.1
    for ti in range(3500):
        EMA = gamma * train_data[ti] + (1 - gamma) * EMA
        train_data[ti] = EMA

    # Used for visualization and test purposes
    all_mid_data = np.concatenate([train_data, test_data], axis=0)

    # Average method estimator
    window_size = 40
    N = train_data.size
    std_avg_predictions = []
    std_avg_x = []
    mse_errors = []

    for pred_idx in range(window_size, N):

        if pred_idx >= N:
            date = dt.datetime.strptime(k, '%d/%m/%Y').date() + dt.timedelta(days=1)
        else:
            date = df.loc[pred_idx, 'date']

        std_avg_predictions.append(np.mean(train_data[pred_idx - window_size:pred_idx]))
        mse_errors.append((std_avg_predictions[-1] - train_data[pred_idx]) ** 2)
        std_avg_x.append(date)

    plt.figure(figsize=(18, 9))
    plt.plot(range(df.shape[0]), all_mid_data, color='b', label='True')
    plt.plot(range(window_size, N), std_avg_predictions, color='orange', label='Prediction')
    # plt.xticks(range(0,df.shape[0],50),df['Date'].loc[::50],rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Mid Price')
    plt.legend(fontsize=18)
    plt.show()
    print('MSE error for standard averaging: %.5f' % (0.5 * np.mean(mse_errors)))

    # Exponential moving average
    window_size = 40
    N = train_data.size

    run_avg_predictions = []
    run_avg_x = []

    mse_errors = []

    running_mean = 0.0
    run_avg_predictions.append(running_mean)

    decay = 0.5

    for pred_idx in range(1, N):
        running_mean = running_mean * decay + (1.0 - decay) * train_data[pred_idx - 1]
        run_avg_predictions.append(running_mean)
        mse_errors.append((run_avg_predictions[-1] - train_data[pred_idx]) ** 2)
        run_avg_x.append(date)

    print('MSE error for EMA averaging: %.5f' % (0.5 * np.mean(mse_errors)))

    plt.figure(figsize=(18, 9))
    plt.plot(range(df.shape[0]), all_mid_data, color='b', label='True')
    plt.plot(range(0, N), run_avg_predictions, color='orange', label='Prediction')
    # plt.xticks(range(0,df.shape[0],50),df['Date'].loc[::50],rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Mid Price')
    plt.legend(fontsize=18)
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
