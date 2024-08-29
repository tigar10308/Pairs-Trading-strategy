import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import  statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from statsmodels.regression.rolling import RollingOLS


tickers = ['META','AMZN','AAPL','NFLX','GOOG']
strat= '2014-01-01'
end= '2015-01-01'

data= yf.download(tickers,strat,end)['Adj Close']

data.info()

def find_cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix= np.zeros((n,n))
    pvalue_matrix= np.ones((n,n))
    keys= data.keys()
    pairs= []
    for i in range(n):
        for j in range(i+1,n):
            S1 = data[keys[i]]
            S2= data[keys[j]]
            result= coint(S1,S2)
            score= result[0]
            pvalue= result[1]
            score_matrix[i,j]=score
            pvalue_matrix[i,j]=pvalue
            if pvalue < 0.05:
                pairs.append((keys[i],keys[j]))
    return score_matrix,pvalue_matrix,pairs

scores,pvalues,pairs= find_cointegrated_pairs(data)

sns.heatmap(
pvalues,
xticklabels= tickers,
yticklabels= tickers,
cmap= 'RdYlGn_r',
mask = (pvalues>=0.05)
)
plt.show()

S1 = data.AMZN
S2= data.AAPL

S1= sm.add_constant(S1)
results= sm.OLS(S2,S1).fit()
S1 = S1.AMZN
b = results.params['AMZN']
spread= S2 - b * S1

spread.plot()
plt.axhline(spread.mean(),color= 'black')
plt.legend(['Spread']);
plt.grid(True)
plt.show()

def  zscore(series):
    return (series-series.mean())/np.std(series)
zscore(spread).plot()
plt.axhline(zscore(spread).mean(),color= 'black')
plt.axhline(-1,linestyle= '--',color='Green',label ='-1')
plt.axhline(1,linestyle= '--',color='Red',label= '+1')
plt.legend(['Spread zscore','mean','-1','+1'])
plt.grid(True)
plt.show()

trades = pd.concat([zscore(spread),S2-b*S1],axis=1)
trades.columns= ["signal","position"]

trades["side"]= 0.0
trades.loc[trades.signal <= -1, "side"]= 1
trades.loc[trades.signal >= 1, "side"]= -1

returns = trades.position.pct_change()*trades.side
returns.cumsum().plot()
plt.show()
