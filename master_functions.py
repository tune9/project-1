'''
Import statements

'''

import requests
import json
import csv

import pandas as pd
import numpy as np

import datetime

from holoviews.plotting.links import RangeToolLink
import holoviews as hv

import plotly.graph_objects as go
from plotly.subplots import make_subplots



'''
Function definitions

'''


def get_stock_data(ticker, api_key):
    
    '''Function to get stock data from the alpha vantage api
    Parameters used are ticker and api key
    The function creates csv files under the Data folder'''


    
    
    #returns data from March to April
    url_month1 = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={ticker}&interval=60min&apikey={api_key}&datatype=json&slice=year1month1'

    r_month1 = requests.get(url_month1)


    #returns data from February to March
    url_month2 = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={ticker}&interval=60min&apikey={api_key}&datatype=json&slice=year1month2'

    r_month2 = requests.get(url_month2)
    
    decoded_content_month1 = r_month1.content.decode('utf-8')
    decoded_content_month2 = r_month2.content.decode('utf-8')
    
    file_name_month_1 = f'Data/data_month_1_{ticker}.csv'
    file_name_month_2 = f'Data/data_month_2_{ticker}.csv'
    
    with open(file_name_month_1, 'w') as file:
        file.write(decoded_content_month1)


    with open(file_name_month_2, 'w') as file:
        file.write(decoded_content_month2)

        
def get_stock_data_volatility(ticker, api_key, month_slice):
    
    '''Function to get stock data for computing volatility from the alpha vantage api
    Parameters used are ticker and api key
    The function creates csv files under the Data folder'''
    
    
    #returns data from March to April
    url_month = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={ticker}&interval=5min&apikey={api_key}&datatype=json&slice={month_slice}'

    r_month = requests.get(url_month)

    decoded_content_month = r_month.content.decode('utf-8')
    
    
    file_name_month = f'Data/Volatility/{ticker}_data.csv'
    
    
    with open(file_name_month, 'w') as file:
        file.write(decoded_content_month)

        
def get_crypto_data(ticker):
    '''Function to get crypto data from the coingecko api
    Parameters used are ticker(crypto id)
    The function creates csv files under the Data folder'''
        
    #calculate unix time stamp for now
    #calculate 60 days unix time stamp from now
    
    date_time_now_epoch = int(datetime.datetime.now().timestamp())
    date_time_60days_epoch = date_time_now_epoch - 60*86400
     
    
    url = f"https://api.coingecko.com/api/v3/coins/{ticker}/market_chart/range?vs_currency=usd&from={date_time_60days_epoch}&to={date_time_now_epoch}"

    r=requests.get(url)
    
    decoded_response = r.content.decode('utf-8')
    response_json = json.loads(decoded_response)
    df = pd.DataFrame(response_json)

    df_prices = df["prices"]
    df_volumes = df["total_volumes"]

    clean_df_prices = pd.DataFrame({"time":[], "close":[]})
    clean_df_volumes = pd.DataFrame({"time":[], "volume":[]})



    for price_index, each in df_prices.iteritems():

            time = Convert_UnixTime_to_ISO(df_prices[price_index][0])
            price = df_prices[price_index][1]

            clean_df_prices.loc[price_index] = [time, price]

    for volume_index, each in df_volumes.iteritems():

            time = Convert_UnixTime_to_ISO(df_volumes[volume_index][0])
            volume = df_volumes[volume_index][1]

            clean_df_volumes.loc[volume_index] = [time, volume]

    clean_df_prices = clean_df_prices.set_index("time")

    clean_df_volumes = clean_df_volumes.set_index("time")



    combined_crypto_df = clean_df_prices.join(clean_df_volumes, on="time")
    
    crypto_file_path = f'Data/data_{ticker}.csv'
    
    combined_crypto_df.to_csv(crypto_file_path)
    

def Convert_UnixTime_to_ISO(unix_time):
    
    '''converts unix time/epochs to ISO format

    parameters used are time in epochs(unix format)

    returns the time in ISO format'''
    
    date_converted = datetime.datetime.utcfromtimestamp(unix_time/1000)  #converting milliseconds to seconds
    
    return date_converted 



def compute_rsi(df, period=14):
    
    '''Computes relative strength index
    parameters are stock and crypto dataframes and average period(14)
    returns the original dataframe with added rsi column'''
    
    delta = df['close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)

    ema_up = up.ewm(com=period -1, adjust=False).mean()
    ema_down = down.ewm(com=period-1, adjust=False).mean()

    rs = ema_up/ema_down
    df['RSI'] = 100 - (100/(1 + rs))
    #df.dropna(inplace=True)
    
    return df



def compute_ewm(df, periods=[20, 50, 200]):
    
    '''Computes exponential weighted mean
    parameters are stock and crypto dataframes and average period(20, 50, 200)
    returns the original dataframe with added ewm_$period column'''
    
    for period in periods:
        
        df[f'ewm_{period}'] = df['close'].ewm(com=period-1, ignore_na=True).mean()
#     df.dropna(inplace=True)
    
    return df




def load_stock_data(ticker):
    
    '''Loading stock data from csv files
    parameter is the ticker symbol
    returns the ticker dataframe'''
    
    file_name_month_1 = f'Data/data_month_1_{ticker}.csv'
    file_name_month_2 = f'Data/data_month_2_{ticker}.csv'
    
    df_month_1 = pd.read_csv(file_name_month_1, parse_dates=['time'], infer_datetime_format=True)
    df_month_1.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    
    df_month_2 = pd.read_csv(file_name_month_2, parse_dates=['time'], infer_datetime_format=True)
    df_month_2.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    
    df = pd.concat([df_month_2, df_month_1], axis=0)
    
    df = df.sort_values(by='date')
    df = df.reset_index().drop(columns=['index'])
    df = df.reset_index().drop(columns=['index'])
    
    return df
    
def load_stock_data_volatility(ticker):
    
    '''Loading stock data from csv files for volatility
    parameter is the ticker symbol
    returns the ticker dataframe'''
    
    file_name = f'Data/Volatility/{ticker}_data.csv'
    
    
    df = pd.read_csv(file_name, parse_dates=['time'], infer_datetime_format=True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    
        
    df = df.sort_values(by='date')
    df = df.reset_index().drop(columns=['index'])
    df = df.reset_index().drop(columns=['index'])
    
    return df    


def plot_stock_rsi(df, period=14):
    
    '''Plots the RSI for stocks.
    Takes dictionary of dataframes, index of NaN values, 
    ticker symbol and prediod defaulted to 14'''
    
    overview = df.hvplot.ohlc(yaxis=None, height=200, fields={'date': 'Date'})
    volume = df.hvplot.step('date', 'volume', color='green', height=150, xaxis=None)
    rsi = df.hvplot.step('date','RSI', grid=True, xaxis=None)
    ohlc = df.hvplot.ohlc(ylabel='Price ($)', grid=True, xaxis=None)
    ewm = df.hvplot.line('date',f'ewm_{period}',xaxis=None)
    
    RangeToolLink(overview.get(0), ohlc.get(0))
    
    hline_70 = hv.HLine(70)
    hline_70.opts(
        color='red', 
        line_width=1,
    )
    
    hline_30 = hv.HLine(30)
    hline_30.opts(
        color='green',  
        line_width=1.0,
    )
    
    layout = (volume + ohlc*ewm + rsi*hline_30*hline_70 + overview).cols(1)
    
    layout.opts(merge_tools=True)
    return layout 



def plot_crypto_rsi(df, period=14):
    '''Plots the RSI for crypto.
    Takes a dataframe for crypto'''
    # add subplot properties when initializing fig variable
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01, 
                        row_heights=[0.1,0.2,0.3, 0.5])
    
    
    # Plot volume trace on 1st row 
    fig.add_trace(go.Scatter(x=df.index, 
                            y=df['volume'], 
                            name='Volume',
                            fill='tozeroy',
                            line_color='indigo'
                            ),row=1, col=1)
    
    
    # Plot RSI trace on 2nd row
    fig.add_trace(go.Scatter(x=df.index, 
                             y=df['RSI'], 
                             opacity=1, 
                             line=dict(color= '#fb9f3a', width=2),  
                             name='RSI'), row=2, col=1)
    fig.add_hline(y=70,
                  line=dict(color='red', width=2), 
                  row=2,
                  col=1)
    fig.add_hline(y=30,
                  line=dict(color='green', width=2), 
                  row=2,
                  col=1)
    
    # Plot MACD trace on 3rd row
    colors = ['green' if val >= 0 
          else 'red' for val in df.MACD_hist]

    fig.add_trace(go.Bar(x=df.index, 
                            y=df.MACD_hist,
                            opacity=1,
                            marker_color=colors,
                            name='MACD_Histogram'
                        ), 
                        row=3,
                        col=1
                 )
    fig.add_trace(go.Scatter(x=df.index, 
                                y=df.MACD,
                                name='MACD',
                                line=dict(color='black', width=2)
                            ), 
                          row=3,
                          col=1
                 )
    fig.add_trace(go.Scatter(x=df.index, 
                                y=df.MACD_signal,
                                name='MACD_Signal',
                                line=dict(color='blue', width=1)
                            ), 
                            row=3,
                            col=1
                 )
    
    # Plot Crypto Price on 4th subplot (using the codes from before)
    
    fig.add_trace(go.Scatter(x=df.index, 
                             y=df['close'], 
                             opacity=1, 
                             line=dict(color='#005CAB',width=2),
                             fill=None,
                             name='Price'
                            ),
                            row=4,
                            col=1
                 )
    
    fig.add_trace(go.Scatter(x=df.index, 
                                y=df[f'ewm_{period}'], 
                                opacity=0.7, 
                                line=dict(color='#FFC325',width=1),
                                fill='tonexty',
                                name='EWM'
                            ),
                                row=4, 
                                col=1
                 )
    
    
    # update layout by changing the plot size, hiding legends & rangeslider, and removing gaps between dates
    fig.update_layout(height=900, width=1200, 
                      showlegend=True, 
                      xaxis4_rangeslider_visible=True)
    
    # update y-axis label
    fig.update_yaxes(title_text="Price", row=4, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    fig.update_yaxes(title_text="Volume", row=1, col=1)
    fig.update_yaxes(title_text="RSI", showgrid=True, row=2, col=1)
    
    
    # removing white space
    fig.update_layout(margin=go.layout.Margin(
            l=20, #left margin
            r=20, #right margin
            b=20, #bottom margin
            t=20  #top margin
        ))
    return fig


def backtesting_rsi(df, is_crypto=False):
    '''Backtesting for RSI strategy. 
    input dataframe and is_crypto.
    returns:
    list of transactions, 
    balance after each transaction,
    total balance up to date
    '''
    oversold = 30
    overbought = 70
    is_oversold = False
    is_overbought = True
    is_sold = False
    is_bought = False
    
    transactions = []
    balance = []
    current_trade = 0
    
    if is_crypto:
        date_time = 'time'
    else:
        date_time = 'date'
    
    prev_time = df[date_time].iloc[0]
    
    for (rsi, time) in zip(df['RSI'], df[date_time]):
    
        if rsi <= oversold:
            is_oversold = True
            prev_time = time
    #         print('below 30'
    
        elif rsi>= overbought:
        
            is_overbought = True
            prev_time = time
    #         print('above 70')
        else:
            if is_overbought:
#                 print(rsi, 'to sell', df['close'][df['time']==prev_time].iloc[0])
                is_overbought = False
                
                if ~is_sold and is_bought:
                    price = df['close'][df[date_time]==prev_time].iloc[0]
                    transactions.append(['sell', price, prev_time])
                    current_trade += price 
                    balance.append(current_trade)
                    is_sold = True
                    is_bought = False
                    
            if is_oversold:
#                print(rsi, 'to buy', df['close'][df['time']==prev_time].iloc[0])
                is_oversold = False
                if (~is_bought and is_sold) or (len(transactions)==0):
                    price = df['close'][df[date_time]==prev_time].iloc[0]
    
                    transactions.append(['buy', price, prev_time])
                    current_trade = -price
                    is_bought = True
                    is_sold = False
    
            prev_time = time
    return (transactions, balance, sum(balance))