import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quandl

df = quandl.get("BCHAIN/MKPRU", authtoken="9D6DF7xSA-sQGYNqxhG-").reset_index()

dfdate = pd.to_datetime(df["Date"])
dfvalue = df["Value"]



FOURyrMA = dfvalue.rolling(window=1460).mean()

MAslope = FOURyrMA.pct_change()
AVGmaSLOPE = MAslope.rolling(window=365).mean()

risk = MAslope/AVGmaSLOPE
normrisk = (risk - np.min(risk)) / (np.max(risk) - np.min(risk))

plt.style.use("dark_background")




for i in range (0,11):
    if i == 0:
        print(str(10 * i) + " percentile risk value: ")
        print(np.percentile(normrisk[1825:], [10* i]))
        print("")
    else:
        print(str(10*i) + "th percentile risk value: ")
        print(np.percentile(normrisk[1825:], [10*i]))
        print("")



plt.semilogy(dfdate[1400:], dfvalue[1400:], color = "grey", zorder = 0)
plt.semilogy(dfdate, FOURyrMA, color = "green", alpha = 0.4)
plt.scatter(dfdate, dfvalue, c = normrisk, cmap = "turbo", zorder = 1)
plt.plot(dfdate, normrisk, color = "#4259FF")

cbar = plt.colorbar()
cbar.set_label("Bitcoin Derivative Heatmap")
cbar.ax.yaxis.set_label_position("left")

plt.ylabel("BTCUSD Price ($)")


plt.axhline(y=np.percentile(normrisk[1825:], [0]), color = "#0FFF00", linewidth = 3)
plt.axhline(y=np.percentile(normrisk[1825:], [10]), color = "#0FFF00")
plt.axhline(y=np.percentile(normrisk[1825:], [20]), color = "#0FFF00")
plt.axhline(y=np.percentile(normrisk[1825:], [30]), color = "#0FFF00")
plt.axhline(y=np.percentile(normrisk[1825:], [40]), color = "#0FFF00")
plt.axhline(y=normrisk.median())
plt.axhline(y=np.percentile(normrisk[1825:], [60]), color = "#FF2626")
plt.axhline(y=np.percentile(normrisk[1825:], [70]), color = "#FF2626")
plt.axhline(y=np.percentile(normrisk[1825:], [80]), color = "#FF2626")
plt.axhline(y=np.percentile(normrisk[1825:], [90]), color = "#FF2626")
plt.axhline(y=np.percentile(normrisk[1825:], [100]), color = "#FF2626", linewidth = 3)


#make backtesting protocol
#set period of time to DCA and give total return
#lump sum at period of time, give total return


startDate = 1850
usdInput = 50
interval = 15
print("")
print("============================================================================================================================================================")
print("============================================================================================================================================================")
print("")

print("PARAMETERS FOR ACCUMULATION TEST:")
print("")
print("Starting date:")
print(dfdate[startDate])
print("")
print("FOR LUMP SUM: ")
print("Initial investment:")
print(int(((len(dfvalue) - startDate) / interval) * usdInput))
print("")
print("FOR STATIC DCA:")
print("Input in USD:")
print(usdInput)
print("Interval of investment (days):")
print(interval)
print("")
print("FOR RISK BASED DCA:")
print("Input in USD:")
print(usdInput)
print("Interval of investment (days):")
print(interval)




print("")
print("============================================================================================================================================================")
print("============================================================================================================================================================")
print("")
print("LUMP SUM")

lsusdInput = int(((len(dfvalue) - startDate) / interval) * usdInput)
def lumpSUM(startDate, lsusdInput):
    bitcoin = lsusdInput/dfvalue[startDate]
    startVAL = bitcoin * dfvalue[startDate]
    currentVAL = bitcoin * dfvalue[len(dfvalue) - 1]
    return startVAL, bitcoin, currentVAL

lsStartVal, lsbitcoin, lsCurrentVal = lumpSUM(startDate, lsusdInput)


print("Amount of bitcoin accumulated with lump sum: ")
print(lsbitcoin)
print("")


print("Current value of Bitcoin accumulated (USD): ")
print(lsCurrentVal)
print("")

print("Percent return with lump sum: ")
print(lsCurrentVal/lsStartVal * 100)

#Static DCA Protocol


def staticDCA(startDate, interval, usdInput):
    cost = 0
    bitcoin = 0
    while startDate < len(dfvalue):
        bitcoin = bitcoin + usdInput / dfvalue[startDate]
        startDate = startDate + interval
        cost = cost + usdInput
    return bitcoin, cost


sbitcoin, scost = staticDCA(startDate, interval, usdInput)

print("")
print("============================================================================================================================================================")
print("============================================================================================================================================================")
print("")


print("STATIC DCA")


print("")
print("Amount of bitcoin accumulated with static DCA: ")
print(sbitcoin)
print("")



USDvalDCA = sbitcoin * dfvalue[len(dfvalue) - 1]

print("Current value of Bitcoin accumulated (USD): ")
print(USDvalDCA)

print("")
print("Percent return with static DCA: ")
print(USDvalDCA/scost * 100)
print("")



#200WMA risk based DCA


def riskBasedDCA(startDate, interval, usdInput):
    cost = 0
    bitcoin = 0
    while startDate < len(dfvalue):
        if normrisk[startDate] < np.percentile(normrisk[1825:], [10])[0]:
            bitcoin = bitcoin + 2.00 * usdInput / dfvalue[startDate]
            cost = cost + 2 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [20])[0]:
            bitcoin = bitcoin + 1.75 * usdInput / dfvalue[startDate]
            cost = cost + 1.75 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [30])[0]:
            bitcoin = bitcoin + 1.50 * usdInput / dfvalue[startDate]
            cost = cost + 1.50 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [40])[0]:
            bitcoin = bitcoin + 1.25 * usdInput / dfvalue[startDate]
            cost = cost + 1.25 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [50])[0]:
            bitcoin = bitcoin + usdInput / dfvalue[startDate]
            cost = cost + 1.00 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [60])[0]:
            bitcoin = bitcoin + usdInput / dfvalue[startDate]
            cost = cost + 1.00 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [70])[0]:
            bitcoin = bitcoin + 0.75 * usdInput / dfvalue[startDate]
            cost = cost + 0.75 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [80])[0]:
            bitcoin = bitcoin + 0.50 * usdInput / dfvalue[startDate]
            cost = cost + 0.50 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [90])[0]:
            bitcoin = bitcoin + 0.25 * usdInput / dfvalue[startDate]
            cost = cost + 0.25 * usdInput
        elif normrisk[startDate] < np.percentile(normrisk[1825:], [100])[0]:
            bitcoin = bitcoin + 0 * usdInput / dfvalue[startDate]
        startDate = startDate + interval
    return bitcoin, cost


rbitcoin, rcost = riskBasedDCA(startDate, interval, usdInput)


print("============================================================================================================================================================")
print("============================================================================================================================================================")
print("")


print("RISK BASED DCA")
print("")
print("Average Cost with risk based DCA: ")
print(rcost/scost * usdInput)
print("")



print("Amount of bitcoin accumulated with risk based DCA: ")
print(rbitcoin)
print("")

USDvalrDCA = rbitcoin * dfvalue[len(dfvalue) - 1]

print("Current value of Bitcoin accumulated (USD): ")
print(USDvalrDCA)
print("")


print("Percent return with risk based DCA: ")
print(USDvalrDCA / rcost * 100)


print("")
print("Risk DCA %return / Static DCA %return: ")
print(rbitcoin / sbitcoin)
print("")


def backtesting(startDate):
    creturns = 0
    count = 1
    backtest = []
    while startDate < len(dfvalue):
        rb, x = riskBasedDCA(startDate, interval, usdInput)
        sb, y = staticDCA(startDate, interval, usdInput)
        creturns = creturns + rb/sb - 1
        areturn = rb/sb - 1
        backtest.append(areturn)
        startDate = startDate + 100
        count = count + 1
    return creturns, count, backtest


creturns, count, backtest = backtesting(startDate)







print("============================================================================================================================================================")
print("============================================================================================================================================================")

print("")
print("AVERAGE COMPARED RETURNS")
print("(positive value indicates average percent outperformance of risk based DCA over static DCA)")
print(creturns/count * 100)
print("")

print("STANDARD DEVIATION OF COMPARED RETURNS (in %)")
print(np.std(backtest) * 100)
print("")

print("WORST % PERFORMANCE RELATIVE TO STATIC DCA RETURNS")
print(np.amin(backtest) * 100)
print("")

print("BEST % PERFORMANCE RELATIVE TO STATIC DCA RETURNS")
print(np.amax(backtest) * 100)
print("")


print("============================================================================================================================================================")
print("============================================================================================================================================================")


print("")
print("RISK BASED DCA SIGNALS: ")
print("")


if normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [10])[0]:
    print("Signals to buy 2.00x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [20])[0]:
    print("Signals to buy 1.75x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [30])[0]:
    print("Signals to buy 1.50x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [40])[0]:
    print("Signals to buy 1.25x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [50])[0]:
    print("Signals to buy 1.00x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [60])[0]:
    print("Signals to buy 1.00x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [70])[0]:
    print("Signals to buy 0.75x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [80])[0]:
    print("Signals to buy 0.50x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [90])[0]:
    print("Signals to buy 0.25x DCA")
elif normrisk[len(dfvalue) - 1] < np.percentile(normrisk[1825:], [100])[0]:
    print("Signals to buy 0x DCA")


plt.show()



