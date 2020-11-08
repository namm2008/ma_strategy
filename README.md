# Moving Average Strategy
Backtesting Moving average strategies.
Differ from a Simple Moving Average (SMA), an Exponential Moving Average (EMA) is a type of moving average (MA) giving higher weighting to the more recent data points. It used a recursive method for the calculation. As EMA put more weight on the recent data, it can better trace the price momentum with the market fluctuation. 


## Trading Strategy
The trading strategies is to use two different period EMA lines to generate buy and sell signals. The shorter period EMA lines (EMA short) and longer period EMA line (EMA long) was plotted with the price shown. When the EMA short cross above the EMA long, it will be a buying signal. Otherwise, it will be a selling signal. The basic working principle of this strategy was that the market will keep on its upward or downward trend for an uncertain time period. This is the momentum of the price due to the market ambience. When the EMA short pass the EMA long, the signal of upward trend is confirmed.
