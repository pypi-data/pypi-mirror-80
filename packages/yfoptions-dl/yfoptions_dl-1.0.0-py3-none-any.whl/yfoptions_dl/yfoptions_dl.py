import requests
import json
import datetime as dt
import pandas as pd
import sqlite3


class optionChain:

    def __init__(self, symbol:str = None, date:int = None):
        self.url = 'https://query2.finance.yahoo.com/v7/finance/options/'
        self.symbol = symbol
        self.r = self.request_data(symbol, date)
        self.data_header= ['contractSymbol','strike','currency','lastPrice',
                           'change','percentChange','volume','openInterest',
                           'bid','ask','contractSize','expiration','lastTradeDate',
                           'impliedVolatility','inTheMoney']
        

        self.data, self.expiration_dates_unix, self.strikes, self.has_mini, self.quote, self.option_chain = self.parse_response(self.r)
        self.expiration_dates = [self._convert_date(date) for date in self.expiration_dates_unix]
        self.calls, self.puts = self.parse_all_options()
        


    def _convert_date(self, unix_date):
        return dt.datetime.utcfromtimestamp(unix_date)


    def request_data(self, symbol:str = None, date:int = None):
        if date == None:
            r = requests.get(rf'{self.url}{self.symbol}')
        elif date != None:
            r = requests.get(rf'{self.url}{self.symbol}?date={date}')
        return r


    def parse_response(self, response):
##        print(response)
        data = json.loads(response.text)['optionChain']['result'][0]
        expiration_dates_unix = data['expirationDates']
        strikes = data['strikes']
        has_mini = data['hasMiniOptions']
        quote = data['quote']
        try:
            option_chain = data['options'][0]
        except:
            raise SymbolDNEError(self.symbol)
            
        return data, expiration_dates_unix, strikes, has_mini, quote, option_chain

        
##    def _get_calls(self):
##        return self.option_chain['calls']
##
##
##    def _get_puts(self):
##        return self.option_chain['puts']


    
    def parse_option_data(self, data):
        
        big_dict = {}
        for key in self.data_header:
            big_dict[key] = []
            for d in data:
                try:
                    big_dict[key].append(d[key])
                except:
                    big_dict[key].append(None)
                    
        df = pd.DataFrame(big_dict)
        df['expiration'] = pd.to_datetime(df['expiration'], unit = 's')
        df['lastTradeDate'] = pd.to_datetime(df['lastTradeDate'], unit = 's')
        df['date'] = dt.datetime.today()
        
        return df

    def parse_all_options(self):
        df_calls=pd.DataFrame()
        df_puts=pd.DataFrame()
        for date in self.expiration_dates_unix:
            r = self.request_data(self.symbol, date)
            _,_,_,_,_,option_chain = self.parse_response(r)
            calls = option_chain['calls']
            puts = option_chain['puts']
            df_calls = df_calls.append(self.parse_option_data(calls))
            df_calls['type']='C'
            df_puts = df_puts.append(self.parse_option_data(puts))
            df_puts['type']='P'
        return df_calls, df_puts

    
    def save_to_sql(self, db_dst, table_name):
        conn = sqlite3.connect(db_dst)
        self.calls.to_sql(table_name, conn, if_exists='append',index=False)
        self.puts.to_sql(table_name, conn, if_exists='append',index=False)
        
        

class SymbolDNEError(Exception):
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return f"The symbole '{self.symbol}' does not exist."
