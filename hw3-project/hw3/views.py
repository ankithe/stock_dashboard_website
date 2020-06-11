from django.shortcuts import render
import statistics
import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

def home(request): 
    print("home")
    return render(request, 'home.html')

def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num


def monte_carlo_simulation(request):
    style.use('ggplot')

    ticker_symbol = request.GET['tikr_symbol'].strip()
    length_of_forecast = float(request.GET['duration'].strip())
    years_of_data = float(request.GET['data'].strip())
    #years_of_data = 5


    #Looking at the data from past 5 years
    end = dt.datetime.today()

    start = end - dt.timedelta(days=years_of_data*365)

    try:
        prices = web.DataReader(ticker_symbol, 'yahoo', start, end).reset_index()['Close']
        returns = prices.pct_change()
    except:
        message = "Error: " + ticker_symbol.upper + " is an invalid ticker symbol."
        data = {
            # 'estimate': end_of_year_estimation,
            # 'tikr_symbol': ticker_symbol.upper(),
            'message': message
        }
        return render(request, 'home.html', data)



    last_price = prices[len(prices) - 1]

    # Number of Simulations
    num_of_simulations = 1000
    projection_duration = round(252*length_of_forecast)

    simulation_df = pd.DataFrame()

    for x in range(num_of_simulations):
        count = 0
        daily_volatility = returns.std()
        avg_daily_returns = returns.mean()

        price_series = []

        price = last_price * (1 + np.random.normal(avg_daily_returns, daily_volatility))  # shock constant
        price_series.append(price)

        for y in range(projection_duration - 1):
            # if count == 251:
            #     break
            price = price_series[count] * (1 + np.random.normal(avg_daily_returns, daily_volatility))  # shock constant
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    end_of_year_averages = simulation_df.values[-1].tolist()
    end_of_year_estimation = statistics.mean(end_of_year_averages)
    print("Estimated Price: " + str(round(end_of_year_estimation)))

    # fig = plt.figure()
    # fig.suptitle('Monte Carlo Simulation: ' + ticker_symbol)
    # plt.plot(simulation_df)
    # plt.axhline(y=last_price, color='r', linestyle='-')
    # plt.xlabel('Day')
    # plt.ylabel('Price')
    # plt.savefig('monte_carlo_simulation.png')

    length_of_forecast = formatNumber(length_of_forecast)
    if length_of_forecast == 1:
        message = ticker_symbol.upper() + " price target for " + str(length_of_forecast) + " year: " + str(
            round(end_of_year_estimation, 2))
    else:
        message = ticker_symbol.upper() + " price target for " + str(round(length_of_forecast,2)) + " years: " + str(
            round(end_of_year_estimation, 2))
    data = {
        # 'estimate': end_of_year_estimation,
        # 'tikr_symbol': ticker_symbol.upper(),
        'message': message
    }

    return render(request, 'home.html', data)


