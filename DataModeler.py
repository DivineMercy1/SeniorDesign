# Connection lib to mysql server
import mysql.connector
# Used for plotting data
import matplotlib.pyplot as plt
# Project files
import LocalLibrary as ll
import DataTransmitter as dt

# Machine learning libraries
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import warnings
import itertools
import numpy as np
import os
import datetime
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
import matplotlib

# setting the plot settings
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

# Plots the data in the table for the given metric
def DataPlot(dataSet):
    # Gets rid of the ' UTC' ending of the timestamp values
    dataSet['timestamp'] = dataSet['timestamp'].map(lambda x : x.lstrip('').rstrip(' UTC'))
    # Sets the dataframe's indexing to the timestamp
    dataSet = dataSet.set_index(pd.DatetimeIndex(dataSet['timestamp']))
    dataSet.index
    # Column 0 is the value, Column 1 is the timestamp
    dataSet.head()
    dataSet.describe()
    dataSet.info()
    # Look at the graph that shows the line trend of data
    dataSet.plot(kind = "line")
    #
    #plt.show()
    # the y axis will be the values sampled at a frequency of business days 'B', averaged
    y = dataSet['values'].resample('B').mean()
    #y = y.dropna()
    #print(y['2018':])

    # Show the plot of the data we have
    y.plot(figsize=(14,8))
    #plt.show()
    return y

# Plots sarimax graphs. Dataset is what the graph reads in to train. iterator is the metric it is viewing. predictionDate is the date to start forecasting from.
def SARIMAXPlot(dataSet, iterator, predictionDate):
    #perform SARIMAX analysis, seasonal autoregressive integrated moving average
    # TODO - make ARIMA analysis
    #p = q = d = range(0,2)
    #pdq = list(itertools.product(p,d,q))
    #seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p,d,q))]
    mod = sm.tsa.statespace.SARIMAX(dataSet, order = (1,1,1), seasonal_order=(1,1,0,12), enforce_stationarity=False, enforce_invertibility=False)

    #mod = ARMA(y, order = (1,1,1))
    results = mod.fit()
    print(results.summary().tables[1])
    results.plot_diagnostics(figsize=(16,8))
    plt.savefig("images/" + metrics[iterator] + " - SARIMAX.png")
    dt.AddEmailImage("images/" + metrics[iterator] + " - SARIMAX.png")
    plt.show()

    #validate forecasts
    # TODO - start datetime will change in future as data is fed in, the forecast will be using newer timedate
    pred = results.get_prediction(start=pd.to_datetime(predictionDate), dynamic=False)
    pred_ci = pred.conf_int()
    ax = y[str(datetime.datetime.strptime(predictionDate, '%Y-%m-%d').year):].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-Step ahead forecast', alpha = 7, figsize=(14,8))
    ax.fill_between(pred_ci.index, pred_ci.iloc[:,0], pred_ci.iloc[:,1], color = 'k', alpha = .2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    plt.legend()
    #exports
    plt.savefig("images/" + metrics[iterator] + " - one-step ahead forecast.png")
    dt.AddEmailImage("images/" + metrics[iterator] + " - one-step ahead forecast.png")
    plt.show()
    return pred.predicted_mean, results

# Performs an analysis of stepsAhead intervals, where the sampling rate is set in DataPlot(). dataSet is what is used to graph,
# results is what the forecast is drawn from. startDate is the sample start date to begin forecasting at.
def DataAnalysis(dataSet, results, iterator, stepsAhead, startDate):
    # get a forecasted value
    y_forecasted = dataSet
    y_truth = y[startDate:]
    # Mean squared error, and RMSE
    mse = ((y_forecasted - y_truth) ** 2).mean()
    # estimator of the average squared difference between the estimated values and what is estimated
    dt.AddEmailText('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
    #print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
    # RMSE - that our model was able to forecast the average values in the test set within x of the real values.
    #print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))
    dt.AddEmailText('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

    # Producing and visualizing forecasts
    pred_uc = results.get_forecast(steps=stepsAhead)
    pred_ci = pred_uc.conf_int()
    ax = y.plot(label='observed', figsize=(14, 8))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Motor RPM Pullout Value')
    plt.legend()
    plt.savefig("images/" + metrics[iterator] + " - 15 step ahead.png")
    dt.AddEmailImage("images/" + metrics[iterator] + " - 15 step ahead.png")
    plt.show()
    #dt.SendEmails("test.png")

    pred_mean = np.mean(pred_uc.predicted_mean)
    pred_sd = np.std(pred_uc.predicted_mean)
    #print('Predicted mean = ' + str(pred_mean))
    #print('Predicted standard deviation = ' + str(pred_sd))
    dt.AddEmailText('Predicted mean = ' + str(pred_mean))
    dt.AddEmailText('Predicted standard deviation = ' + str(pred_sd))
    sendEmail = False
    i = 0
    for row in pred_uc.predicted_mean:
        if (row < (pred_mean - pred_sd/2)):
            lowPoint = row
            break
        i = i + 1
    if (lowPoint is not None):
        j = 0
        for row in pred_ci.itertuples():
            if(i == j):
                #print('Sensed instability for future date: {}'.format(row[0]))
                dt.AddEmailText('Sensed instability for future date: {}'.format(row[0]))
                sendEmail = True
                break
            j = j + 1
    if (sendEmail):
        recip = []
        dataT.setQuery(ll.GetEmails())
        dataT.performQuery()
        for x in cursor:
            x = ''.join(x)
            recip.append(x)
        dt.AddEmailRecipients(recip)
        dt.SendEmails()
    return pred_uc.predicted_mean, pred_ci

# uploads the forcasted information to the server
# predData1 contains the actual forecastetd value, predData2 contains the date, lower and upper value
def UploadForecast(predData1, predData2, metric, steps):
    # vals = [steps][5]
    # steps refers to the amount of stepsAhead that was forecasted
    vals =[[0 for x in range( 5 )] for y in range( steps )]
    # grabs the value
    for i in range(0, len(predData1)):
        vals[i][0]= predData1.iloc[i]
    i = 0
    # gets timestamp, lower value, upper value, metric name
    for row in predData2.itertuples():
        vals[i][1] = '{}'.format(row[0])
        vals[i][2] = row[1]
        vals[i][3] = row[2]
        vals[i][4] = metric
        i = i + 1
    # loop through arrayt and upload to server
    c = dataT.getPreparedCursor()
    for row in vals:
        dataT.setQuery(ll.InsertForecast())
        # parameterized query, refer to InsertForecast()
        c.execute(dataT.getQuery(), (row[0], row[1], row[2], row[3], row[4],))
        dataT.comm()

# sets up the data transmitter, connects to server
dataT = dt.DatabaseClient()
cursor = dataT.getCursor()
# ------------TODO------------------------
# - Retrieve the Oden data with api      -
# - Import that data to relevant table   -
# - Limit the data you want to watch     -
# - i.e. time range (say last 3 months)  -
# ------- END TODO -----------------------

# Shows all databases that can be used
dataT.setQuery("show databases;")
dataT.performQuery()
for x in cursor:
    print(x)

# We are using the oden data
dataT.setQuery("use odendata;")
dataT.performQuery()

# metric variables we track
# identified as markers that signify downtime
metrics = []
dataT.setQuery(ll.GetMetrics())
dataT.performQuery()
for x in cursor:
    x = ''.join(x)
    metrics.append(x)

# go through all of the metric variables we are watching
for metric in range(0, len(metrics)):
    # since we grab files for the train info, we want to delete the training file if it exists
    ll.DeleteCSVFile(metrics[metric])
    # Get and export data to a CSV file.
    dataT.setQuery(ll._selectColumnHeaders + ll.SelectMetric(metrics[metric]) + ll.OutputToFileNameQuery(metrics[metric]))
    dt.AddEmailText("Query used: " + dataT._currentQuery)
    #print(dataT._currentQuery)
    # Saves the CSV file
    dataT.performQuery()
    # set trainSet to be a pandas dataframe so we can work with it
    trainSet = pd.read_csv('dump/' + metrics[metric] + '.csv')
    # refer to the three methods above to see what each does.
    y = DataPlot(trainSet)
    pred, results = SARIMAXPlot(y, metric, '2018-10-01')
    predD1, predD2 = DataAnalysis(pred, results, metric, 15, '2018-11-01')

    # upload CSVs to database which gets read through power bi.
    UploadForecast(predD1, predD2, metrics[metric], 15)

    ll.DeleteImageFolder('images/')
dataT.setQuery(ll.ClearForecast())
dataT.performQuery()
dataT.close()