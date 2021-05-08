###############################################################
# Program:
#     Stock trader.
#
# Authors:
#     Mike Sosa
#
# Summary:
#    This program will connect to Webull app, ask for a symbol 
#     analyze Support/Resistance lines, and place Buy/Sell 
#     orders for that symbol. 
#
# Coding Time:
#     18 hours
#
###############################################################

#API's libraries for the type of account and buying/selling actions
from webull import webull, endpoints # for 'paper' money trading, just import 'paper_webull' instead
from webull.streamconn import StreamConn
import paho.mqtt.client as mqtt

#All this imports are tools to graph the support/resistance lines
import json
import trendln
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.interactive(True)

import numpy as np
import pandas as pd

from datetime import datetime
import sched
import time

#Variables 
symbol = None
period = None
timeframe = None
hist = []

print("Logging in to WeBull...")
####################################################################
# All the login part of the code starts from here
####################################################################
wb = webull()
f = None
loginInfo = None
try:
    f = open("token.txt", "r")
    loginInfo = json.load(f)
except:
    print("First time login.")
hist = None
support = 0
resistance = 0
enteredTrade = False
s = sched.scheduler(time.time, time.sleep)

#If first time save login as token
if not loginInfo:
    wb.get_mfa('kaabal@protonmail.com') # Mobile number should be okay as well.
    code = input('Enter MFA Code : ')   #2FA code required 
    loginInfo = wb.login('kaabal@protonmail.com', '79RG3hwBRMP9xb', 'Webull Bot', code)
    f = open("token.txt", "w")  #This will access token.txt
    f.write(json.dumps(loginInfo)) #This will store the token from line #66 for future logins 
    f.close()
else:
    wb.refresh_login()
    loginInfo = wb.login('kaabal@protonmail.com', '79RG3hwBRMP9xb')

####################################################################
# This part of the code creates the chart of the symbol with the 
# specific time frame user provides
####################################################################
def drawChart(hist, update):
    global support
    global resistance
    global symbol
    try :
        mins, maxs = trendln.calc_support_resistance((hist[-1000:].low, hist[-1000:].high))
        support = mins[1][1]
        resistance = maxs[1][1]
        print("Current Support : ", support, " Will buy once " + symbol.upper() + " reaches this number.")
        print("Current Resistance : ", resistance)
        minimaIdxs, maximaIdxs = trendln.get_extrema((hist[-1000:].low, hist[-1000:].high))
        fig = trendln.plot_sup_res_date((hist[-1000:].low, hist[-1000:].high), hist[-1000:].index)
        fig.canvas.set_window_title(symbol.upper() + " Bot")
        fig.suptitle(symbol.upper() + " Support/Resistance Lines")
        plt.draw()
    except Exception as e:
        print('')

####################################################################
# This part of the code will retrieve suport and resistance from 
# drawChart and will place a BUY or a SELL order in Webull according
# the support or resistance prices.
####################################################################
def run(sc):
    global hist
    global enteredTrade
    global symbol
    global timeframe
    global period
    global s
    hist = pd.DataFrame(hist)
    try:
        #Get current low and high
        low = hist.iloc[len(hist) - 1,2]
        high = hist.iloc[len(hist) - 1,1]
        if(low > 0):
            #Buy at support
            if (low <= support and not enteredTrade):
                order = wb.place_order(stock=symbol.upper(), action='BUY', orderType='MKT', enforce='DAY', quant=1)
                print(order)
                enteredTrade = True
            #Sell at resistance
            if (high >= resistance and enteredTrade):
                order = wb.place_order(stock=symbol.upper(), action='SELL', orderType='MKT', enforce='DAY', quant=1)
                print(order)
                enteredTrade = False
            #Update chart with new data
            hist = wb.get_bars(stock=symbol.upper(), interval='m'+timeframe, count=int((390*int(period))/int(timeframe)), extendTrading=0)
            hist = pd.DataFrame(hist)
            #call this method again every minute for new price changes
            drawChart(hist, True)
    except Exception as e:
        print(str(e))
    s.enter(60, 1, run, (sc,))
    plt.pause(60)
conn = StreamConn(debug_flg=False)
if not loginInfo['668529'] is None and len(loginInfo['668529']) > 1:
    conn.connect(loginInfo['uuid'], access_token=loginInfo['668529'])
else:
    conn.connect(wb.did)