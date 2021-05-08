# Overview

This is the first attempt to create a trading bot. The program has three main obejctives or purposes: 
 
    1. **Connect to the desire brocker** (Webull in this case) from the terminal.
    2. **Generate a graphic analysis** of specific candlesticks timeframe and calculate the Support and Resistance lines.
    3. Store the Support and Resistance lines to **place a BUY or SELL order from this program** into the account with the broker. 

Unfortunately, by the time of the publish of this repository there is not and official API from Webull. 

[Software Demo Video](http://youtube.link.goes.here)

# Development Environment

* VScode
* Python version 3.9.2
* [Unofficial Webull API by tedchou12](https://github.com/tedchou12/webull)
* Pytest

### Libraries
* [Matplot Library version 3.4.2](https://matplotlib.org/)

# Useful Websites

* [Heads up to this amazing source written by Gregory Morse that crack up how to graph Support and Resistance points in Python. Such a life saver!](https://towardsdatascience.com/programmatic-identification-of-support-resistance-trend-lines-with-python-d797a4a90530)
* [Geeks for geeks](https://www.geeksforgeeks.org/python-programming-language/)

# Future Work

* The log in feature can change in the future and the partially works and sometimes it doesn't connect to the Webull app. I definately have to put more time in working with it.
* Start developing machine learning with other math equations for data analysis and prediction.
* Live updates on candlesticks with a specific time of a Symbol. 
* Make a Windows exceutable program
