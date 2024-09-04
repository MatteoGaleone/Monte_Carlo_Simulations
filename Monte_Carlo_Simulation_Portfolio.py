import yahoo_fin.stock_info as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

def input_parameters():    
    t = []
    w = []
    nt = int(input('Insert number of assets:'))
    for i in range(nt):
        ticker = str(input('''Insert ticker of the asset number ''' + str(i) + ':'))
        weight= float(input('''Insert weight of the asset (e.g. 0.5)  ''' + ticker + ':'))
        t.append(ticker)
        w.append(weight)
    return t, w

def download_multiplicative_returns(t, start=str(datetime.now() - timedelta(days=900)), end = str(datetime.now()), period = '1d'):
    matrix_returns=pd.DataFrame()
    for x in t:
        stock_data = yf.get_data(x, start_date = start, end_date = end, interval = period)
        stock_data = stock_data['close']
        matrix_returns[x]=(stock_data/stock_data.shift(1)).dropna() 
    return matrix_returns

def bootstrap_time_series(starting_wealth, num_steps, w, matrix_returns):
    time_series = []
    daily_returns = []
    
    bootstrap_returns = matrix_returns.sample(num_steps)
    daily_returns = bootstrap_returns.dot(w) 
    
    time_series.append(starting_wealth)
    for i in range(len(daily_returns)):
        d = time_series[i]*daily_returns[i]
        time_series.append(d)
        
    return time_series

#Input parameters
t, w = input_parameters()

#Download the matrix with the daily returns of every asset
matrix_returns = download_multiplicative_returns(t)

plt.figure(figsize=(25,15))

#Setting default parameters for MC simulations
starting_wealth = 100
num_simulations = 1000
num_steps = 100
end_wealth = []

#Simulate portfolio path, store end wealth for mean and plot time series
for i in range(0, num_simulations):
    time_series = bootstrap_time_series(starting_wealth, num_steps, w, matrix_returns)
    end_wealth.append(time_series[-1])
    
    plt.plot(time_series)
    

#Compute mean and media of the portfolio
mean = str(round(np.mean(end_wealth), 2))
median = str(round(np.median(end_wealth), 2))

#Plot mc simulations and histogram
plt.figure(figsize = (25,15))
plt.hist(end_wealth, bins=200)
plt.title('mean '+ mean +', median='+ median , fontsize=22)
plt.savefig('MC_sim.png')
plt.show()
