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
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
import matplotlib

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

# sets up the data transmitter, connects to server
dataT = dt.DatabaseClient()
cursor = dataT.getCursor()

# metric variables we track
metrics = ["motorrpmpullout", "motorloadmetering"]
# Shows all databases that can be used
dataT.setQuery("show databases;")
dataT.performQuery()
for x in cursor:
    print(x)
# We are using the oden data
dataT.setQuery("use odendata;")
dataT.performQuery()
# since we grab files for the train info, we want to delete the training file if it exists
ll.DeleteCSVFile(metrics[0])
# Get and export data to a CSV file.
dataT.setQuery(ll._selectColumnHeaders + ll.SelectMetric(metrics[0]) + ll.OutputToFileNameQuery(metrics[0]))
print(dataT._currentQuery)
# Saves the CSV file
dataT.performQuery()

trainRPM = pd.read_csv(metrics[0] + '.csv')
# Gets rid of the ' UTC' ending of the timestamp values
trainRPM['timestamp'] = trainRPM['timestamp'].map(lambda x : x.lstrip('').rstrip(' UTC'))
# Sets the dataframe's indexing to the timestamp
trainRPM = trainRPM.set_index(pd.DatetimeIndex(trainRPM['timestamp']))
trainRPM.index
print (trainRPM)
# Column 0 is the value, Column 1 is the timestamp
trainRPM.head()
trainRPM.describe()
trainRPM.info()
# Look at the graph that shows the line trend of data
trainRPM.plot(kind = "line")
plt.show()
# the y axis will be the values sampled at a frequency of business days 'B', averaged
y = trainRPM['values'].resample('B').mean()
#y = y.dropna()
print(y['2018':])

# Show the plot of the data we have
y.plot(figsize=(14,8))
plt.show()

#perform ARIMA analysis, autoregressive integrated moving average
p = q = d = range(0,2)
pdq = list(itertools.product(p,d,q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p,d,q))]
mod = sm.tsa.statespace.SARIMAX(y, order = (1,1,1), seasonal_order=(1,1,0,12), enforce_stationarity=False, enforce_invertibility=False)

#mod = ARMA(y, order = (1,1,1))
results = mod.fit()
print(results.summary().tables[1])
results.plot_diagnostics(figsize=(16,8))
plt.show()


#validate forecasts
pred = results.get_prediction(start=pd.to_datetime('2018-10-01'), dynamic=False)
#from datetime import date
#from datetime import datetime
#pred = results.predict(start = datetime.combine('2018-11-01', time()), end = datetime.combine('2019-01-01', datetime.min.time()), dynamic=False)
pred_ci = pred.conf_int()
ax = y['2018':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-Step ahead forecast', alpha = 7, figsize=(14,8))
ax.fill_between(pred_ci.index, pred_ci.iloc[:,0], pred_ci.iloc[:,1], color = 'k', alpha = .2)
ax.set_xlabel('Date')
ax.set_ylabel('Values')
plt.legend()
plt.show()

# get a forecasted value
y_forecasted = pred.predicted_mean
y_truth = y['2018-11-01':]
# Mean squared error, and RMSE
mse = ((y_forecasted - y_truth) ** 2).mean()
# estimator of the average squared difference between the estimated values and what is estimated
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
# RMSE - that our model was able to forecast the average values in the test set within x of the real values.
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

# Producing and visualizing forecasts
pred_uc = results.get_forecast(steps=15)
pred_ci = pred_uc.conf_int()
ax = y.plot(label='observed', figsize=(14, 8))
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('Motor RPM Pullout Value')
plt.legend()
plt.savefig("test.png")
plt.show()
#dt.SendEmails("test.png")

pred_mean = np.mean(pred_uc.predicted_mean)
pred_sd = np.std(pred_uc.predicted_mean)
print('Predicted mean = ' + str(pred_mean))
print('Predicted standard deviation = ' + str(pred_sd))
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
            print('Sensed instability for future date: {}'.format(row[0]))
            break
        j = j + 1
pred_ci.to_csv("testOutput.csv")
pred_uc.predicted_mean.to_csv("testOutput1.csv")
dataT.close()