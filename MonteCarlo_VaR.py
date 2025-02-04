import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import time

#function for fetching stock data
def get_data(stocks, start, end):
    stockData = yf.download(stocks, start=start, end=end)['Close']

    #checking to see if the data is empty
    if stockData.empty:
        print("Error: No stock data retrieved.")
        return None, None

    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns, covMatrix


stocklist = ['TSLA', 'NVDA', 'AAPL', 'ZOMATO.BO']

#range for the date
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=300)
time.sleep(1)

#fetching the data
meanReturns, covMatrix = get_data(stocklist, startDate, endDate)


if meanReturns is not None:
    meanReturns_df = pd.DataFrame(meanReturns, columns=["Mean Daily Return"])
    print(meanReturns_df)

#assigning random weights to the portfolio
weights= np.random.random(len(meanReturns))
weights /= np.sum(weights)

#Monte Carlo Method
#define number of simulations
mc_sims= 100
T=100 #timeframe in days

meanM= np.full(shape=(T,len(weights)),fill_value=meanReturns)
meanM=meanM.T

portfolio_sims= np.full(shape=(T,mc_sims),fill_value=0.0)

initialPortfolio=10000

for m in range(0,mc_sims):
    #MC loops
    #Using Cholesky distribution
    Z=np.random.normal(size=(T,len(weights)))
    L=np.linalg.cholesky(covMatrix) #works out the lower triangle for Cholesky distribution
    dailyReturns= meanM + np.inner(L,Z)
    portfolio_sims[:,m]=np.cumprod(np.inner(weights,dailyReturns.T)+1)*initialPortfolio

#plotting
plt.plot(portfolio_sims)
plt.ylabel('Porfolio Value ($)')
plt.xlabel('Days')
plt.title('MC Simulation of a Stock Portfolio')
plt.savefig("monte_carlo_simulation.png", dpi=300)
plt.show()

#defining a Value at Risk function

def mcVaR(returns, alpha=5):
    #input: pandas series of returns
    #outputs:percentile on return distribution to a given confidence level alpha 
    if isinstance(returns,pd.Series):
        return np.percentile(returns,alpha)
    else:
        raise TypeError("Expected a pandas data series.")
    
def mcCVaR(returns, alpha=5):
    #input: pandas series of returns
    #outputs:CVaR or expected shortfall to a given confidence level alpha 
    if isinstance(returns,pd.Series):
        belowVaR = returns <= mcVaR(returns,alpha=alpha)
        return returns[belowVaR].mean()
    else:
        raise TypeError("Expected a pandas data series.")
    
#now we want to return the value of each portfolio_sims at the very last time stamp

portResults= pd.Series(portfolio_sims[-1,:])

VaR=initialPortfolio- mcVaR(portResults,alpha=5)
CVaR= initialPortfolio- mcCVaR(portResults,alpha=5)

print("VaR ${}".format(round(VaR,2)))
print("CVaR ${}".format(round(CVaR,2)))

    



