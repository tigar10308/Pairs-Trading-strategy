# Pairs-Trading-strategy
This project implements a cointegration-based pairs trading strategy using Python. The strategy identifies pairs of stocks that are likely to revert to a mean relationship and uses this relationship to make trading decisions.

#Data Collection: 
From Yahoo Finance , covering the period from January 1, 2014 to january 1 2015

#Cointegration Analysis:
The find_cointegrated_pairs function identifies pairs of stocks that are cointegrated, meaning they have a stable long-term relationship. A heatmap visualizes the p-values of the cointegration tests, highlighting pairs that are likely to revert to a mean relationship.

#Spread Calculation:
For a selected pair (AMZN and AAPL) the spread between the two stock is calculated using linear regression.This spread is the basis for trading decisions.

#Zscore calculation:
The spread is normalized using Zscore allowing us to quantify how far the current spread is from it mean. This zscore is used to generate trading signals.

#Tradimg signal and Backtesting:
trading signals are generated based on the zscore 
Buy whem the Zscore is below -1 
Sell whn the Zscore is above +1

The strategy performance is backtested with cumulative returns plotted to evaluate is profitability 
