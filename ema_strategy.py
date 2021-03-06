# Import all the required libraries
import seaborn as sns
import plotly.express as px
import datapackage
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt

class ema_strategy():
    
    ''' 
    start: start time, e.g. '1998-01-01'
    end: end time, e.g. '2019-12-31'
    ticker: stock ticker in NYSE, e.g. 'F'
    ema_short: Days of period for shorter EMA, e.g. 9
    ema_long: Days of period for longer EMA, e.g. 40
    tolerance_day: tolerance day after the EMA line intercept before trading, e.g. 2
    commission: commission rate for each transaction, e.g. 0.25
    short_sell: allow short selling, e.g. False
    train_test_ratio: train test ratio if you use for maschine learning backtesting, e.g. 0.1
    '''
    
    def __init__(self, start, end, ticker, train_test_ratio):
        self.start = start
        self.end = end
        self.ticker = ticker
        self.train_test_ratio = train_test_ratio
        
    def data_loader(self,ema_short, ema_long, tolerance_day, commission, short_sell=True):
        # Get data from CSV file
        self.ema_short = ema_short
        self.ema_long = ema_long
        self.tolerance_day = tolerance_day
        self.commission = commission
        self.short_sell = short_sell
        
        # Get data from 'yahoo'
        self.df = web.DataReader(self.ticker, 'yahoo', self.start, self.end)
        
        #self.df = self.data_loader(self.start, self.end, self.ticker)
        self.df['ema_short'] = self.df['Close'].ewm(span=ema_short, adjust=False).mean()
        self.df['ema_long'] = self.df['Close'].ewm(span=ema_long, adjust=False).mean()
        self.df['diff_ema'] = self.df['ema_short'] - self.df['ema_long']
        self.df['pct_change'] = self.df['Close'].pct_change()
        self.df['Ones'] = 1  # for finding SD
        self.df['buy_sell'] = 0
        dataset_len = len(self.df)
        test_length = round(self.train_test_ratio*dataset_len)
        df_test = self.df.iloc[-test_length:,:].reset_index(drop=True)
        df_train = self.df.iloc[:(-test_length),:]
        self.train_end = str(df_train.index[-1])[:10]
        return df_train, df_test
        
    def strategy(self, df):
        buy = 0
        sell = 0
        toler_pos = 0
        toler_neg = 0
    
        self.df_buy_sell = pd.DataFrame(columns = ['Date', 'Buy_sell', 'Price'])
        # list of the conditions for buying and selling

        if self.short_sell == True:
            for i in range(len(df)):
                if i != len(df)-1:
                    if df['diff_ema'][i] >= 0 and buy == 0 and sell == 0:
                        toler_pos += 1
                        if toler_pos >= self.tolerance_day + 1:
                            date = df.index[i]
                            buysell = 'Buy'
                            price = df['Close'][i]
                            record = {'Date':date,'Buy_sell':buysell,'Price':price}
                            self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                            toler_pos = 0
                            buy = 1
                            #print('Buy long at {} at {}'.format(date, price))
                        else: pass
                    elif df['diff_ema'][i] < 0 and buy == 0 and sell == 0:
                        toler_neg += 1
                        if toler_neg >= self.tolerance_day+1:
                            date = df.index[i]
                            buysell = 'Sell'
                            price = df['Close'][i]
                            record = {'Date':date,'Buy_sell':buysell,'Price':price}
                            self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                            toler_neg = 0
                            sell = 1
                            #print('Short sell at {} at {}'.format(date, price))
                        else: pass
        
                    elif df['diff_ema'][i] >= 0 and buy == 1 and sell == 0:
                        pass
                    elif df['diff_ema'][i] < 0 and buy == 0 and sell == 1:
                        pass
        
                    elif df['diff_ema'][i] < 0 and buy == 1 and sell == 0:
                        toler_neg += 1
                        toler_pos = 0
                        date = df.index[i]
                        buysell = 'Sell'
                        price = df['Close'][i]
                        record = {'Date':date,'Buy_sell':buysell,'Price':price}
                        self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                        buy = 0
                        sell = 0
                        #print('Sell(zero) at {} at {}'.format(date, price))
                    elif df['diff_ema'][i] > 0 and buy == 0 and sell == 1:
                        toler_pos += 1
                        toler_neg = 0
                        date = df.index[i]
                        buysell = 'Buy'
                        price = df['Close'][i]
                        record = {'Date':date,'Buy_sell':buysell,'Price':price}
                        self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                        buy = 0
                        sell = 0
                        #print('Buy(zero) at {} at {}'.format(date, price))
                else:
                    if buy == 0 and sell == 0:
                        pass
                    if buy == 1:
                        date = df.index[i]
                        buysell = 'Sell'
                        price = df['Close'][i]
                        record = {'Date':date,'Buy_sell':buysell,'Price':price}
                        self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                    elif sell == 1:
                        date = df.index[i]
                        buysell = 'Sell'
                        price = df['Close'][i]
                        record = {'Date':date,'Buy_sell':buysell,'Price':price}
                        self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
        
        elif self.short_sell == False:
            for i in range(len(df)):
                if i != len(df)-1:
                    if df['diff_ema'][i] >= 0 and buy == 0:
                        toler_pos += 1
                        if toler_pos >= self.tolerance_day + 1:
                            date = df.index[i]
                            buysell = 'Buy'
                            price = df['Close'][i]
                            record = {'Date':date,'Buy_sell':buysell,'Price':price}
                            self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                            toler_pos = 0
                            buy = 1

                    elif df['diff_ema'][i] < 0 and buy == 1:
                        date = df.index[i]
                        buysell = 'Sell'
                        price = df['Close'][i]
                        record = {'Date':date,'Buy_sell':buysell,'Price':price}
                        self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                        buy = 0
                else:

                    if buy == 1:
                        date = df.index[i]
                        buysell = 'Sell'
                        price = df['Close'][i]
                        record = {'Date':date,'Buy_sell':buysell,'Price':price}
                        self.df_buy_sell = self.df_buy_sell.append(record, ignore_index=True)
                df['buy_sell'][i] = buy
        return df
    

        #return dataframe with [date, buy/sell, price] and PnL
        #return self.df_buy_sell
    
    def com_neg(self, price_df):
        price_ = price_df - self.commission/100*price_df
        return price_
    
    def com_pos(self, price_df):
        price_ = price_df + self.commission/100*price_df
        return price_        
    
    def trade_statistics(self, df):
        self.df_each_trade_pnl = pd.DataFrame(columns = ['Date', 'Long_short', 'PnL'])
        record = {'Date':0, 'Long_short':'Long', 'PnL':0}
        self.df_each_trade_pnl = self.df_each_trade_pnl.append(record, ignore_index=True)
        for i in range(0,len(self.df_buy_sell), 2):
            if self.df_buy_sell['Buy_sell'][i] == 'Buy':
                date = self.df_buy_sell['Date'][i+1]
                longshort = 'Long'
                pnl = (self.com_neg(self.df_buy_sell['Price'][i+1]) - 
                       self.com_pos(self.df_buy_sell['Price'][i]))/self.com_pos(self.df_buy_sell['Price'][i])
                record = {'Date':date, 'Long_short':longshort, 'PnL':pnl}
                self.df_each_trade_pnl = self.df_each_trade_pnl.append(record, ignore_index=True)
            elif self.df_buy_sell['Buy_sell'][i] == 'Sell':
                date = self.df_buy_sell['Date'][i+1]
                longshort = 'Short'
                pnl = (self.com_neg(self.df_buy_sell['Price'][i]) - 
                       self.com_pos(self.df_buy_sell['Price'][i+1]))/self.com_pos(self.df_buy_sell['Price'][i+1])
                record = {'Date':date, 'Long_short':longshort, 'PnL':pnl}
                self.df_each_trade_pnl = self.df_each_trade_pnl.append(record, ignore_index=True)           
    
        self.df_each_trade_pnl['ones'] = 1
        self.df_each_trade_pnl['cum_pnl'] = self.df_each_trade_pnl['PnL'] + self.df_each_trade_pnl['ones']
        self.df_each_trade_pnl['cum_pnl'] = self.df_each_trade_pnl['cum_pnl'].cumprod()
    
        #Find Standard Deviation:
        sd_df = df[['pct_change','Ones','buy_sell']]
        sd_df['percent'] = sd_df['pct_change']*sd_df['buy_sell']
        sd_df['cum_perf'] = (sd_df['percent']+1).cumprod()
        SD = sd_df['cum_perf'].std()
        
        
        Num_year = round(len(df)/253,1)
        num_trade = len(self.df_buy_sell)
        tran_per_year = num_trade/Num_year

        print('Total number of trading days = {}'.format(len(df)))
        print('Number of years = {}'.format(Num_year))
        print('Trasaction Number = {}'.format(num_trade))
        print('Transaction per Year = {:.2f}'.format(tran_per_year))
        df['cum_performance'] = (df['pct_change'] + 1).cumprod()
        
        if num_trade == 0:
            win_ratio = 0
            sharpe_ratio = 0
            max_drawdown = 0
            max_return = 0
            under_total_return = 0
            under_annual_return = 0
            model_total_return = 0
            model_annual_return = 0
            
        else:                                                                                                                              
            win = len(self.df_each_trade_pnl[self.df_each_trade_pnl['PnL'] > 0])
            loss = len(self.df_each_trade_pnl[self.df_each_trade_pnl['PnL'] < 0])
            win_ratio = win/(win+loss+0.001)        
            max_drawdown = self.df_each_trade_pnl['cum_pnl'].min()
            max_drawdown = (max_drawdown - 1)*100
    
            max_return = self.df_each_trade_pnl['cum_pnl'].max()
            max_return = (max_return - 1)*100
        
            under_total_return = df['cum_performance'].iloc[-1] - 1
            under_annual_return =  (under_total_return+1)**(1/Num_year) - 1
            model_total_return = self.df_each_trade_pnl['cum_pnl'].iloc[-1] -1
            model_annual_return = (model_total_return+1)**(1/Num_year) - 1
            sharpe_ratio = model_total_return/(SD+0.001)
        
        #for constructing holding graph
        df['new_buy'] = df['buy_sell']*df['cum_performance']
        for i in range(len(df)):
            if df['buy_sell'].iloc[i] == 0:
                df['new_buy'].iloc[i] = None
        
        print('Win Ratio = {:.5f}%\nMaximum Drawdown = {:.5f}%\nMaximum Return = {:.5f}%'.format(win_ratio*100, 
                                                                                                 max_drawdown,
                                                                                                 max_return))        
        print('Sharpe Ratio = {:.5f}'.format(sharpe_ratio))
        print('Underlying Total Return = {:.5f}%'.format(under_total_return*100))
        print('Underlying Annualized Return = {:.5f}%'.format(under_annual_return*100))
        print('Model Total Return = {:.5f}%'.format(model_total_return*100))
        print('Model Annualized Return = {:.5f}%'.format(model_annual_return*100)) 
                                                
        return [len(df),
                Num_year,
                num_trade,tran_per_year,
                win_ratio*100,
                max_drawdown,  
                max_return,
                sharpe_ratio,
                under_total_return*100,
                under_annual_return*100,
                model_total_return*100,
                model_annual_return*100]
    
    def plot_trade(self, train_test):
        plt.figure(figsize=(15,8))
        plt.grid()
        plt.plot(self.df_each_trade_pnl['Date'], (self.df_each_trade_pnl['cum_pnl'] - 1)*100, label = 'Performance')
        if train_test == 'Training':
            plt.title(self.ticker + ' Performance from ' + self.start + ' to ' + self.train_end)
        else:
            plt.title(self.ticker + ' Performance from ' + self.train_end + ' to ' + self.end)
        plt.xlabel('Time')
        plt.ylabel('Percentage')
        plt.legend()
        plt.show()
    
    def plot_under_model(self, df, train_test):
        plt.figure(figsize=(15,8))
        plt.grid()
        plt.plot(self.df_each_trade_pnl['Date'], (self.df_each_trade_pnl['cum_pnl'] - 1)*100, label = 'Model')
        plt.plot((df['cum_performance'] -1)*100, label = 'Underlying')
        plt.plot((df['new_buy'] -1)*100, label = 'Holding', marker = 'x')
        if train_test == 'Training':
            plt.title(self.ticker + ' Performance from ' + self.start + ' to ' + self.train_end)
        else:
            plt.title(self.ticker + ' Performance from ' + self.train_end + ' to ' + self.end)
        plt.xlabel('Time')
        plt.ylabel('Percentage')
        plt.legend()
        plt.show()        
        