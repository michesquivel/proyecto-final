# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 17:26:28 2022

@author: MICH
"""


from numpy import asarray
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
from matplotlib import pyplot
 
# transform a time series dataset into a supervised learning dataset
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(values) is list else values.shape[1]
	df = DataFrame(data)
	cols = list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
	# put it all together
	agg = concat(cols, axis=1)
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg.values
 
# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
	return data[:-n_test, :], data[-n_test:, :]
 
# fit an xgboost model and make a one step prediction
def xgboost_forecast(train, testX):
	# transform list into array
	train = asarray(train)
	# split into input and output columns
	trainX, trainy = train[:, :-1], train[:, -1]
	# fit model
	model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
	model.fit(trainX, trainy)
	# make a one-step prediction
	yhat = model.predict(asarray([testX]))
	return yhat[0]
 
# walk-forward validation for univariate data
def walk_forward_validation(data, n_test):
	predictions = list()
	# split dataset
	train, test = train_test_split(data, n_test)
	# seed history with training dataset
	history = [x for x in train]
	# step over each time-step in the test set
	for i in range(len(test)):
		# split test row into input and output columns
		testX, testy = test[i, :-1], test[i, -1]
		# fit model on history and make a prediction
		yhat = xgboost_forecast(history, testX)
		# store forecast in list of predictions
		predictions.append(yhat)
		# add actual observation to history for the next loop
		history.append(test[i])
		# summarize progress
		print('>expected=%.1f, predicted=%.1f' % (testy, yhat))
	# estimate prediction error
	error = mean_absolute_error(test[:, -1], predictions)
	return error, test[:, -1], predictions
 
# load the dataset

series1 = read_csv('C:/Users/MICH/Downloads/Venta Historíca 7 Tiendas Qro.csv')

import pandas as pd
series1['FECHA'] = pd.to_datetime(series1['KEYFIGUREDATE'])

a = series1[series1['CUSTID']=='T4721']
# T2082
# T2084
# T4183
# T4721
# T5898
# T9787
# T9510
# T9379

a=a.groupby(by=['FECHA'])['ACTUALSQTY'].sum().to_frame()


# values = series.values

values = a.values


# transform the time series data into supervised learning
data = series_to_supervised(values, n_in=52)
# evaluate
mae, y, yhat = walk_forward_validation(data, 30)
print('MAE: %.3f' % mae)
# plot expected vs preducted
pyplot.plot(y, label='Expected')
pyplot.plot(yhat, label='Predicted')
pyplot.legend()
pyplot.show()

# finalize model and make a prediction for monthly births with xgboost
from numpy import asarray
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from xgboost import XGBRegressor
 
# transform a time series dataset into a supervised learning dataset
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols = list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
	# put it all together
	agg = concat(cols, axis=1)
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg.values
 
# load the dataset
#series = read_csv('C:/Users/MICH/Downloads/Venta Historíca 7 Tiendas Qro.csv')

series = a
values = series.values
# transform the time series data into supervised learning
train = series_to_supervised(values, n_in=52)
# split into input and output columns
trainX, trainy = train[:, :-1], train[:, -1]
# fit model
model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)
model.fit(trainX, trainy)
# construct an input for a new preduction
row = values[-52:].flatten()
# make a one-step prediction
import numpy
yhat = model.predict(asarray([row]),10)
predi=0
i=1
for i in range(1,16):
    if i==1:
        row1=row
        row1=numpy.append(row1[1:],yhat.astype(int))
    else:
        row1=numpy.append(row1[1:],predi.astype(int))
    predi = model.predict(asarray([row1]))
    row1=numpy.append(row1[1:],predi.astype(int))

df = pd.DataFrame(row, columns = ['Vta'])
df['ok'] = 1

df1 = pd.DataFrame(row1[36:], columns = ['Pred'],index = range(51, 51+16))

pyplot.plot(df['Vta'], label='Expected')
pyplot.plot(df1[:15], label='Predicted')
pyplot.legend()
pyplot.show()


model.score(trainX, trainy)
