https://docs.google.com/presentation/d/1AI9MgTkg9nNMocFFrQsWJK9IHLWC9UWhRIQ-epTOMKc/edit?usp=sharing

# Technical Portfolio Analysis


# Introduction

We are presenting a technical analysis study on baskets of stocks and cryptocurrencies. We used data analysis to determine when market is in a good state to make a trade and used technical indicators to determine long/short bias.


Five stocks were chosen for the stock portfolio. Stocks were chosen after analyzing which are most volatile and attractive for short term trading. We selected from a list of stocks with 7% weekly volatility and one million shares per day average. We then sorted by market cap and took five of the largest. We ended up with Rivian (RIVN), Twitter (TWTR), Doordash (DASH), Unity Software (U), and Cleveland-Cliffs (CLF). 

Five cryptos were chosen based on volatility and market cap. We settled on Bitcoin (BTC), Ethereum (ETH), BinanceCoin (BNB), Solana (SOL), and Cardano (ADA).


# Clean and prepare the data:
APIs used:  
CoinGecko  
Alpha Vantage  

Created module:  
master_functions.py


AlphaVantage API was used to get data for stocks. The function - "TIME_SERIES_INTRADAY_EXTENDED" exposes the timestamp, open, high, low, close prices and the volume of trades during a given day. For computing RSI and EMA the time period for the data was 60 days, while for the volatility 30 days was chosen. Additionally for RSI and EMA the frequency for data analysis was 60 minutes, while for the volatility the frequency chosen was 5 minutes. The AlphaVantage API had a limit on the number of API calls - 5 per minute and 500 per day. To work around this limit, a code pause of 30 seconds was applied when retrieving stock data from a list of stock tickers.
To retrieve data for crypto Coingecko api was utilized. The API exposed time, close and volume data with a frequency of 60 minutes. The API needed time inputs in epochs and 60 days of data was retrieved from the API.[^1] [^2]  

The master_functions.py is a python module, that was created to house resusable methods across the jupyter notebook files. Some of the common tasks that can be performed by the methods are retrieving and processing data from the APIs (stock and crypto), plotting data and conversion of data formats.

# Should we trade?

First, we determined when its a good time to trade. We analyzed the volatility trends and present the information to the end-user. Volatility analysis is done based on a 30 day time period.


Volatility/Price change:  
Volatility is a measure of a stock’s variability from the general trading activity of the SP500, otherwise known as beta. It is defined as a statistical measure of the dispersion of returns for a given security or market index. Equities that have a higher level of volatility are seen to be riskier investments due to their wild swings in value. Volatility periods can also be viewed as the deviation from normal trading activity of that particular equity. Though volatility can be seen as more risky, it can also yield significant returns depending on the positions taken during these periods of volatility.
Statistically, volatility can be calculated either as a standard deviation or variance. For the purposes of our analysis, we’ve taken the standard deviation calculation to determine the most volatile trading period for each particular equity. We used a rolling standard deviation calculation method, collecting 12 price points every hour to calculate hourly standard deviation over a month’s period. We then took the top 25% quantile of our standard deviation data to determine the most volatile periods, and assessed which periods were most volatile for each respective equity and cryptocurrency. With this information, we will determine when to conduct trades in order to obtain as much alpha in our portfolio as possible[^3] [^4].

![Vol1](/Images/Volatility_hvplot2.png)
![Vol2](/Images/Volatility_hvplot5.png)


# What trades should be made?
Trade bias is based on EMA/MACD and RSI analysis. 

EMA: The exponential moving average (EMA) is a type of moving average that places a greater weight and significance on the most recent data points. This technical indicator is used to produce buy and sell signals based on crossovers and divergences from the historical average. The common EMA lengths are 20-day, 50-day and 200-day moving average.
The moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. It is used to identify when bullish or bearish momentum is high in order to identify entry and exit points for trades. Essentially, it calculates the difference between an instrument’s 26-day and 12-day EMA.
Our Strategy:
The MACD generates a bullish signal when it moves above its the MACD signal (9-day EMA) and it generates a self sign when it moves below the MACD signal.

Our EMA/MACD Strategy:
An asset is only considered in a LONG buy if the price is above the 20-day EMA. Likewise, an asset is only considered for a SHORT position if the price is below the 20-day EMA. This strategy enables us to take advantage of assets with strong market momentum[^5].

![EMA](/Images/EMA.png)
![RSI_MACD](/Images/RSI_MACD.png)


RSI: RSI is the Relative Strength Index. The relative strength index (RSI) is a technical indicator used in the analysis of financial markets, that defines strength of the trand and the probability of its change, based on the closing price of the recent trading period.

Te RSI is displayed as an oscillator (a step graph that moves between two extremes) and can have a reading from 0 to 100. Momentum is the rate of the rise or fall in price. The RSI computes momentum as the ratio of higher closes to lower closes: stocks which have had more or stronger positive changes have a higher RSI than stocks which have had more or stronger negative changes.[^6]


Our RSI Strategy:
* Stock is oversold if the value is below 30 and, the stock is over overbought if the value is above 70. Sometimes 80/20 and 90/10 pairs are also used. 

Backtesting:  
* Backtesting shows good results from this strategy. Over the course of the test period, RIVN profit was -$2.52 per share. TWTR profit was $2.97 per share. DASH profit was $43.32 per share. U profit was -$5.02 per share. CLF profit was $7.68 per share. In crypto, SOL profit was $18.89 per coin. BTC profit was $2704.92. ETH profit was $675.35. BNB profit was $58.80. ADA profit was $0.05.

![RSI1](/Images/RSI2.png)

![RSI3](/Images/RSI4.gif)



# Summarizing the strategy

We have created an algorithm with the following parameters.

Go long if all parameters are met:  
1. Volatility is in the top 25 percent of all recorded values.  
2. Last price is above 20 period EMA.  
3. RSI is below 30.  

Go short if all parameters are met:
1. Volatility is in the top 25 percent of all recorded values.  
2. Last price is below 20 period EMA.  
3. RSI value is above 70.  


# Limitations

1. This analysis does not search for optimal entry points for trades.
2. This analysis does not identify optimal conditions for exiting trades.
3. This analysis only utilizes technicals that rely on momentum trading.

# Iteration Opportunities

1. Use this analysis as a foundation for creating a trading bot!


[^1]: https://www.alphavantage.co/documentation/
[^2]: https://www.coingecko.com/en/api/documentation?msclkid=217cc994b83111ec9eb92b1e04a26f4c
[^3]: https://www.investopedia.com/terms/v/volatility.asp#:~:text=Volatility%20is%20a%20statistical%20measure,same%20security%20or%20market%20index.
[^4]: https://web.archive.org/web/20120330224816/http://www.lfrankcabrera.com/calc-hist-vol.pdf
[^5]: https://www.investopedia.com/terms/e/ema.asp 
[^6]: https://en.wikipedia.org/wiki/Relative_strength_index


