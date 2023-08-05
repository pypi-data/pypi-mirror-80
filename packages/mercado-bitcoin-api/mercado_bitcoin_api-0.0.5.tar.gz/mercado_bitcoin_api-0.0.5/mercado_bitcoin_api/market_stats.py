import numpy as np
import pandas as pd
import datetime

class MarketStats:
    def __init__(self):
        self._tickers = {}
        self._orderbooks = {}
        pass
    
    def add_ticker(self, ticker):
        timestamp = datetime.datetime.utcfromtimestamp(ticker['date'])
        columns = ['high', 'low', 'last', 'buy', 'sell', 'open']
        self._tickers[timestamp] = {k: float(ticker[k]) for k in columns}
        return self
        
    def add_orderbook(self, orderbook):
        timestamp = datetime.datetime.utcfromtimestamp(int(orderbook['timestamp']*1e-9))
        self._orderbooks[timestamp] = {'buys': orderbook['bids'], 'sells': orderbook['asks']}
        return self
    
    def add_trades(self, trades):
        self._trades = trades.copy()
        return self
    
    def orderbook_df(self):
        df = pd.DataFrame.from_dict(self._orderbooks, orient='index')
        return df
    
    def ticker_df(self):
        df = pd.DataFrame.from_dict(self._tickers, orient='index')
        return df
    
    def trades_df(self):
        trades_indexed = {trade['tid']: trade for trade in self._trades}
        df = pd.DataFrame.from_dict(trades_indexed, orient='index')
        df.sort_values(by='date', ascending=False)
        df['date'] = df['date'].apply(datetime.datetime.utcfromtimestamp)
        df['acc_vol'] = df['amount'].cumsum()
        
        trades_sell = df[df['type']=='sell']
        trades_buy = df[df['type']=='buy']

        df['vol_rate'] = df['amount']/np.sum(df['amount'])
        df.loc[trades_sell.index, ['type_vol_rate']] = trades_sell['amount']/np.sum(trades_sell['amount'])
        df.loc[trades_buy.index, ['type_vol_rate']] = trades_buy['amount']/np.sum(trades_buy['amount'])
        
        return df
    
    def last_orderbook(self):
        df = self.orderbook_df()
        last_orderbook_entry = df.tail(1).to_dict(orient='index') 
        last_orderbook_timestamp = list(last_orderbook_entry.keys())[0]
        last_orderbook_content = list(last_orderbook_entry.values())[0]
        return [last_orderbook_timestamp, last_orderbook_content]
    
    def last_ticker(self):
        df = self.ticker_df()
        last_ticker_entry = df.tail(1).to_dict(orient='index')
        last_ticker_timestamp = list(last_ticker_entry.keys())[0]
        last_ticker_content = list(last_ticker_entry.values())[0]
        return [last_ticker_timestamp, last_ticker_content]
    
    def volume_trend(self):
        last_orderbook = self.last_orderbook()[1];
        sells = np.asarray(last_orderbook['sells'])
        buys = np.asarray(last_orderbook['buys'])
        sells_vol_total = np.sum(sells, axis=0)[1]
        buys_vol_total = np.sum(buys, axis=0)[1]
        volume_total = np.asarray([buys_vol_total, sells_vol_total])
        volume_normalized = volume_total/np.sum(volume_total)
        return volume_normalized
    
    def present_targets(self):
        last_orderbook = self.last_orderbook()[1];
        sells = np.asarray(last_orderbook['sells'])
        buys = np.asarray(last_orderbook['buys'])
        sells_vol_total = np.sum(sells, axis=0)[1]
        buys_vol_total = np.sum(buys, axis=0)[1]
        
        sells_normalized = sells.copy()
        sells_normalized[:,1] = sells_normalized[:,1]/sells_vol_total
        buys_normalized = buys.copy()
        buys_normalized[:,1] = buys_normalized[:,1]/buys_vol_total
        sells_target = np.sum(np.prod(sells_normalized, axis=1))
        buys_target = np.sum(np.prod(buys_normalized, axis=1))
        return [buys_target, sells_target]
    
    def past_targets(self, units=1):
        tradesDF = self.trades_df()

        tradesDF = tradesDF[tradesDF['acc_vol']<units]

        trades_sell = tradesDF[tradesDF['type']=='sell']
        trades_buy = tradesDF[tradesDF['type']=='buy']

        tradesDF['vol_rate'] = tradesDF['amount']/np.sum(tradesDF['amount'])
        tradesDF.loc[trades_sell.index, ['type_vol_rate']] = trades_sell['amount']/np.sum(trades_sell['amount'])
        tradesDF.loc[trades_buy.index, ['type_vol_rate']] = trades_buy['amount']/np.sum(trades_buy['amount'])
        
        trades_buy = tradesDF[tradesDF['type']=='buy']
        trades_sell = tradesDF[tradesDF['type']=='sell']

        past_buy_target = np.sum(trades_buy['price']*trades_buy['type_vol_rate'])
        past_sell_target = np.sum(trades_sell['price']*trades_sell['type_vol_rate'])

        return [past_buy_target, past_sell_target]

    def price_weighted(self, units=1):
        tradesDF = self.trades_df()
        tradesDF = tradesDF[tradesDF['acc_vol']<units]
        price_weighted = np.sum(tradesDF['price']*tradesDF['vol_rate'])
        return price_weighted
    
    def present_trend(self, mean, units=1):
        target_distances = np.abs(np.asarray(self.present_targets()) - mean)
        target_distances_normalized = target_distances/np.sum(target_distances)
        present_trend = 1.0-target_distances_normalized
        return present_trend
    
    def past_trend(self, mean, units=1):
        target_distances = np.abs(np.asarray(self.past_targets(units)) - mean)
        target_distances_normalized = target_distances/np.sum(target_distances)
        past_trend = 1.0-target_distances_normalized
        return past_trend
    
    def mean_trend(self, mean, past_units=1):
        mean_trend = (self.past_trend(mean, past_units)+self.present_trend(mean))/2
        return mean_trend
    
    def ticker_stats(self):
        last_ticker_entry = self.last_ticker()
        ticker_timestamp = last_ticker_entry[0]
        ticker = last_ticker_entry[1]
        last_price = ticker['last']
        max_buy_price = ticker['buy']
        min_sell_price = ticker['sell']
        bsm = (max_buy_price + min_sell_price)/2
        ticker_stats = {"last": last_price,
                        "buy": max_buy_price,
                        "sell": min_sell_price,
                        "bsm": bsm,
                        "ticker_timestamp": ticker_timestamp}
        return ticker_stats
    
    def all_stats(self):
        ticker_stats = self.ticker_stats()
        last_orderbook = self.last_orderbook()
        volume_trend = self.volume_trend()
        orderbook_timestamp = last_orderbook[0]
        past_trend_unit1 = self.past_trend(ticker_stats['bsm'], units=1)
        past_trend_unit2 = self.past_trend(ticker_stats['bsm'], units=2)
        past_trend_unit3 = self.past_trend(ticker_stats['bsm'], units=3)
        present_trend = self.present_trend(ticker_stats['bsm'])
        mean_trend = self.mean_trend(ticker_stats['bsm'])
        all_stats = {}
        all_stats.update(ticker_stats)
        all_stats.update(dict(zip(['past_buy_trend_unit1', 'past_sell_trend_unit1'], past_trend_unit1)))
        all_stats.update(dict(zip(['past_buy_trend_unit2', 'past_sell_trend_unit2'], past_trend_unit2)))
        all_stats.update(dict(zip(['past_buy_trend_unit3', 'past_sell_trend_unit3'], past_trend_unit3)))
        all_stats.update(dict(zip(['present_buy_trend', 'present_sell_trend'],present_trend)))
        all_stats.update(dict(zip(['mean_buy_trend', 'mean_sell_trend'],mean_trend)))
        all_stats.update(dict(zip(['volume_buy_trend', 'volume_sell_trend'],volume_trend)))
        all_stats.update({"orderbook_timestamp": orderbook_timestamp})
        all_stats.update({"price_weighted_unit1": self.price_weighted(units=1)})
        all_stats.update({"price_weighted_unit2": self.price_weighted(units=2)})
        all_stats.update({"price_weighted_unit3": self.price_weighted(units=3)})
        return all_stats

