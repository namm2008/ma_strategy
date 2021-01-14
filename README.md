# Moving Average Strategy
Backtesting Moving average strategies.
Differ from a Simple Moving Average (SMA), an Exponential Moving Average (EMA) is a type of moving average (MA) giving higher weighting to the more recent data points. It used a recursive method for the calculation. As EMA put more weight on the recent data, it can better trace the price momentum with the market fluctuation. 


## Trading Strategy
The trading strategies is to use two different period EMA lines to generate buy and sell signals. The shorter period EMA lines (EMA short) and longer period EMA line (EMA long) was plotted with the price shown. When the EMA short cross above the EMA long, it will be a buying signal. Otherwise, it will be a selling signal. The basic working principle of this strategy was that the market will keep on its upward or downward trend for an uncertain time period. This is the momentum of the price due to the market ambience. When the EMA short pass the EMA long, the signal of upward trend is confirmed.

## Model Parameters
1. Tickers of stocks \
2. Start Date\
3. End Date\
4. Ema Short Line period\
5. Ema Long Line period\
6. Number of Tolerance Day\
7. Commission rate per trade\
8. Short Selling allowance\
9. Train Test Ratio (for other model comparison purpose)

## Model Analysis with statistics
1. Total number of trading days \
2. Number of years \
3. Trasaction Number\
4. Transaction per Year\
5. Win Ratio \
6. Maximum Drawdown \
7. Maximum Return \
8. Sharpe Ratio \
9. Underlying Total Return \
10. Underlying Annualized Return \
11. Model Total Return \
12. Model Annualized Return

## Model Visualization
1. Model performance line
2. Underlying performance line
3. Period of Holding of stocks by the model
