#now that we have the data make a back tester to check if it will work take the two collumns the price 

def backtester(signals,price, tcost = 0.001):

#Make a quick numpy array to save the money that willbe made for posible value that the stock could be sold at and the cash on hand, start with one dollar so its not empty.

        pos_val = np.zeros(np.shape(price))
        cash    = np.zeros(np.shape(price))
        cash[0] = 1
        
        #loop throgh each day as though we are going through and actually implementing the strategy as we go

        for i,val in enumerate(price):
            
            #if we are on the last day exit the loop we are done.

            if i == len(price)-1:
                break
            
            # if the signal that that day is to sell the on the next day we should have the possible value of the coin, 
            # times the price of the coin times the brokerage costs plus the money we had perviously.
            # We also sell all of the coin that we have so the possible value left to us is zero

            if signals[i] == -1:

                cash[i+1] = (pos_val[i] * val * (1-tcost)) + cash[i]
                pos_val[i+1] = 0
                
            #If the signal that day is to buy, what we will do is take all of the cash that we have, divide it by the cost of the coin to work out how many we can buy
            #factoring in the cost of the brockerage, we then add it to any stock we held from the pervious day

            elif signals[i] == 1:

                pos_val[i+1] = (cash[i] / val)*((1-tcost)) + pos_val[i]
                cash[i+1] = 0
                
            # Lastly we need to define the do nothng clause. this will not make a buy or a sell, we do need to update the position value to be the number of stocks/coins we own times that days price
                
            elif signals[i] == 0:
                
                pos_val[i+1] = pos_val[i]/price[i]*price[i+1]
                cash[i+1] = cash[i]
                
        #then our returns are the amount of cash left each day plus the the price times the amoint of coin that we have

        returns = [a*b for a,b in zip(pos_val,price)] + cash
        
        #lastly we turn this into a data frame too
        
        return pd.DataFrame(returns, index = price.index)
    
def winrate(data,returns):

#make an enmpty list to store the number of trades made that were money making. 

    tps = []

    #take all of the signals excluding the first and last ones

    sigs = data['Signals'][1:-1].values.ravel()

    #take the percentage returns day on day, not sure why we are only including the days where there is some kind of buy trade and not a sell trade

    rets = (returns.pct_change()).shift(1).dropna().values.ravel()

    #Record a posative signal every time a trade is made and it results in a posative return.
    
    for i,val in enumerate(sigs):  
        if (sigs[i] == 1 and rets[i]>0):
            tps.append(1)

    #Possible other signals that might result in gain, such as holding or selling.

#        if (sigs[i] == -1 and rets[i]>0):
#            tps.append(1)
#        if (sigs[i] == 0 and rets[i]>0):
#            tps.append(1)

    # work out the number of posative signals

    signals, counts = np.unique(sigs, return_counts=True )
    possignals = dict(zip(signals,counts))[1]

    #take the number of buy signals that result in a posative return the next day and divide it by the total number of posative sugnals to work out hte true posative score.

    win_rate = sum(tps)/possignals
    return win_rate

def Sharperatio(returns,tradingdays,rrr):
    
    #First thing to do is to work out the percentage change in the returns for the last year, note that depending on what we are trading there
    #might be a different number of trading days, in the case of Bitcoin the default there are 365, for stocks it is usually 255
    
    lastyearreturns = returns.tail(tradingdays).pct_change().dropna()
    
    # Then working out the sharpe ratio, which is defined as the annuklised rate of return minus the garenteed rate of return divided by the standard deviation
    # of hte returns we need to make sure that we multiply by the 
    
    # Note that we are multiplying the standard deviation by the square root of the trading days, this is because it needs to be the annualised
    # Standard deviation, the daily rate.

    
    sharperatio = (lastyearreturns.mean() * tradingdays - rrr)/(lastyearreturns.std()* np.sqrt(tradingdays))
    
    return sharperatio 