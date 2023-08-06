# pseanalytics

**pseanalytics** is a module that enables collection of PSE stock data through web scraping. The purpose of this module is to provide an API for monitoring PSE stock data and allow development of trading algorithms and screeners around basic stock indicators.

## Features
1. Access historical stock data for up to the past year.
2. Screen and identify potential stock trades based on stock indicators.
3. Send email notifications using [yagmail](https://pypi.org/project/yagmail/) when thresholds against your watchlists are breached.

## Indicators
1. close
2. change
3. percent change
4. open
5. low
6. high
7. volume
8. netforeign
9. ema9, ema12, ema20, ema26, ema50, ema52, ema100
10. macd, macds
11. rsi
12. openh, closeh, opent, closet, body

## Screeners 
1. marketsummary
2. macd rossing
3. rsi oversold and overbought
4. three white soldiers
5. marketvolume
