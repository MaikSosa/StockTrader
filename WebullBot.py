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
from datetime import datetime
import sched
import time

#All this imports are tools to graph the support/resistance lines
import json
import trendln
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
matplotlib.interactive(True)
import numpy as np
import pandas as pd

#Variables 
stockname = None
timeframe = None
period = None
data = []
support = 0
resistance = 0
tradeConfirm = False


print("Attempting Connection")
####################################################################
# All the login part of the code starts from here. Most of the code 
# comes from the API 
####################################################################
wb = webull()
token = None
loginInfo = None

try:
    token = open("token.txt", "r")
    loginInfo = json.load(token)
except:
    print("First time login.")

s = sched.scheduler(time.time, time.sleep)
data = None

#If first time save login as token
if not loginInfo:
    wb.get_mfa('Your Email') #You can use the phone number too
    code = input('2FA Code please: ')   #2FA code required 
    wb.get_security('Your email') #get your security question.
    data = wb.login('Your email', 'Password', 'Name for the device', code , '1002', 'Answer to security question') # 6 digits MFA, Security Question ID, Question Answer.
    token = open("token.txt", "w")  #This will access token.txt
    token.write(json.dumps(loginInfo)) #This will store the token from line #66 for future logins 
    token.close()
else:
    wb.refresh_login()
    loginInfo = wb.login('Your email', 'Password')

####################################################################
# This part of the code will retrieve suport and resistance from 
# drawChart and will place a BUY or a SELL order in Webull according
# the support or resistance prices. Parts of this code comes from
# the API 
####################################################################
def run(sc):
    global data
    global tradeConfirm
    global stockname
    global timeframe
    global period
    global s
    data = pd.DataFrame(data)
    try:
        #Get current low and high
        low = data.iloc[len(data) - 1,2]
        high = data.iloc[len(data) - 1,1]
        if(low > 0):
            #Buy at support
            if (low <= support and not tradeConfirm):
                order = wb.place_order(stock=stockname.upper(), action='BUY', orderType='MKT', enforce='DAY', quant=1)
                print(order)
                tradeConfirm = True
            #Sell at resistance
            if (high >= resistance and tradeConfirm):
                order = wb.place_order(stock=stockname.upper(), action='SELL', orderType='MKT', enforce='DAY', quant=1)
                print(order)
                tradeConfirm = False
            #Update chart with new data
            data = wb.get_bars(stock=stockname.upper(), interval='m'+timeframe, count=int((390*int(period))/int(timeframe)), extendTrading=0)
            data = pd.DataFrame(data)
            #call this method again every minute for new price changes
            drawChart(data, True)
    except Exception as e:
        print(str(e))
    s.enter(60, 1, run, (sc,))
    plt.pause(60)

####################################################################
# This part of the code creates the chart of the symbol with the 
# specific time frame user provides
####################################################################
def drawChart(data, update):
    global support
    global resistance
    global stockname
    try :
        mins, maxs = trendln.calc_support_resistance((data[-1000:].low, data[-1000:].high))
        support = mins[1][1]
        resistance = maxs[1][1]
        print("Current Support : ", support, " Will buy once " + stockname.upper() + " reaches this number.")
        print("Current Resistance : ", resistance)
        minimaIdxs, maximaIdxs = trendln.get_extrema((data[-1000:].low, data[-1000:].high))
        fig = trendln.plot_sup_res_date((data[-1000:].low, data[-1000:].high), data[-1000:].index)
        fig.canvas.set_window_title(stockname.upper() + " Bot")
        fig.suptitle(stockname.upper() + " Support/Resistance Lines")
        plt.draw()
    except Exception as e:
        print('')

