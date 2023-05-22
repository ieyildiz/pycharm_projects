import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

dict = {'a':[11,21,31],'b':[12,22,32]}
df=pd.DataFrame(dict)
type(df)
df.head()
df.mean()

