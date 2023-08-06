# yfoptions_dl
`yfoptions_dl` is a Python library for downloading daily option chain data from yahoo finance. Data is retrieved using yahoo finance's API, then parsed into a `pandas` dataframe.



## Installing yfoptions_dl

The easiest way to install `yfoptions_dl` is from Python Package Index using `pip`:

    pip install yfoptions_dl



## Example

  
To get all available data fields:

      aapl = optionChain('aapl')
      >>> aapl.data_header
    ['contractSymbol', 'strike', 'currency', 'lastPrice', 'change', 'percentChange', 'volume', 'openInterest', 'bid', 'ask', 'contractSize', 'expiration', 'lastTradeDate', 'impliedVolatility', 'inTheMoney']



To get all available strikes for the front month options:
    
    >>> aapl.strikes
    [57.5, 58.75, 60.0, 61.25, 62.5, 63.75, 65.0, 66.25, 67.5, 68.75, 70.0, .....]

To get the entire call option chain:

    >>> aapl.calls
             contractSymbol  strike  ...                       date  type
    0   AAPL200925C00057500   57.50  ... 2020-09-22 16:24:11.085367     C
    1   AAPL200925C00058750   58.75  ... 2020-09-22 16:24:11.085367     C
    2   AAPL200925C00060000   60.00  ... 2020-09-22 16:24:11.085367     C
    3   AAPL200925C00061250   61.25  ... 2020-09-22 16:24:11.085367     C
    4   AAPL200925C00062500   62.50  ... 2020-09-22 16:24:11.085367     C
    ..                  ...     ...  ...                        ...   ...
    26  AAPL230120C00180000  180.00  ... 2020-09-22 16:24:15.772460     C
    27  AAPL230120C00185000  185.00  ... 2020-09-22 16:24:15.772460     C
    28  AAPL230120C00190000  190.00  ... 2020-09-22 16:24:15.772460     C
    29  AAPL230120C00195000  195.00  ... 2020-09-22 16:24:15.772460     C
    30  AAPL230120C00200000  200.00  ... 2020-09-22 16:24:15.772460     C
    
    [2119 rows x 17 columns]


To get hte entire put option chain:



 

    >>> a.puts
                 contractSymbol  strike  ...                       date  type
        0   AAPL200925P00057500   57.50  ... 2020-09-22 16:24:11.107355     P
        1   AAPL200925P00058750   58.75  ... 2020-09-22 16:24:11.107355     P
        2   AAPL200925P00060000   60.00  ... 2020-09-22 16:24:11.107355     P
        3   AAPL200925P00061250   61.25  ... 2020-09-22 16:24:11.107355     P
        4   AAPL200925P00062500   62.50  ... 2020-09-22 16:24:11.107355     P
        ..                  ...     ...  ...                        ...   ...
        18  AAPL230120P00140000  140.00  ... 2020-09-22 16:24:15.782454     P
        19  AAPL230120P00150000  150.00  ... 2020-09-22 16:24:15.782454     P
        20  AAPL230120P00155000  155.00  ... 2020-09-22 16:24:15.782454     P
        21  AAPL230120P00160000  160.00  ... 2020-09-22 16:24:15.782454     P
        22  AAPL230120P00200000  200.00  ... 2020-09-22 16:24:15.782454     P
        
        [2016 rows x 17 columns]

