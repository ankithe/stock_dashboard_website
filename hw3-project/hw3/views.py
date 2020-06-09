from django.shortcuts import render
import statistics
import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
#import matplotlib.pyplot as plt
from matplotlib import style

def home(request): 
    print("home")
    return render(request, 'home.html')


def monte_carlo_simulation(request):
    style.use('ggplot')

    ticker_symbol = request.GET['tikr_symbol']
    duration = float(request.GET['duration'])

    #Looking at the data from past 5 years
    end = dt.datetime.today()

    start = end - dt.timedelta(days=5*365)


    prices = web.DataReader(ticker_symbol, 'yahoo', start, end).reset_index()['Close']
    returns = prices.pct_change()

    last_price = prices[len(prices) - 1]

    # Number of Simulations
    num_of_simulations = 1000
    projection_duration = round(252*duration)

    simulation_df = pd.DataFrame()

    for x in range(num_of_simulations):
        count = 0
        daily_volatility = returns.std()
        avg_daily_returns = returns.mean()

        price_series = []

        price = last_price * (1 + np.random.normal(avg_daily_returns, daily_volatility))  # shock constant
        price_series.append(price)

        for y in range(projection_duration):
            if count == 251:
                break
            price = price_series[count] * (1 + np.random.normal(avg_daily_returns, daily_volatility))  # shock constant
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    end_of_year_averages = simulation_df.values[-1].tolist()
    end_of_year_estimation = statistics.mean(end_of_year_averages)
    print("Estimated Price: " + str(end_of_year_estimation))

    data = {
        'estimate': end_of_year_estimation,
        'tikr_symbol': ticker_symbol.upper()
    }

    return render(request, 'home.html', data)


