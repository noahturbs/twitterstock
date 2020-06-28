import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import models
from keras import optimizers
from keras import layers
import pandas as pd
import csv
import math
import sys
sys.path.append("../")
from datetime import time
import pandas as pd
import pandas_market_calendars as mcal
import datefinder
import re, datetime
import arrow
#   date+time | num | num | num

nyse = mcal.get_calendar('NYSE')
with open('/Users/nbt20/OneDrive/Desktop/elontweets.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    tweets=[]

    schedule = nyse.schedule(start_date='2012-11-16', end_date='2017-09-29')
    early = nyse.schedule(start_date='2012-11-16', end_date='2017-09-29')



    for row in readCSV:
        #print(tweets)
        timestamp=row[0]
        #['2012-11-19 8:59:46']
        match = re.search('\d{4}-\d{2}-\d{2}', timestamp)
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        #format of '2002-12-04'
        if(nyse.open_at_time(early, pd.Timestamp(date.isoformat() + ' 12:00:00', tz='America/New_York'))):

            col0 = date.isoformat()
            #print(type(col0)) this is a string
            col1 = row[1]
            col2 = row[2]
            col3 = row[3]
            col4 = row[4]


            #date1=date("")
            tweets.append([col0,col1,col2,col3,col4])

#print(tweets[0][0])
#print(tweets[1][0])
#print(tweets[2][0])
#ok so now tweets list only contains dates that were open when the stock market was open.

with open('/Users/nbt20/OneDrive/Desktop/mhpython/elonstocks.csv') as otherfile:
    readCSV = csv.reader(otherfile, delimiter=',')
    stocks =[]
    stockindexing=[]


    for row in readCSV:
        #print(tweets)
        timestamp=row[0]
        #['2012/11/19']
        #format of '2002-12-04'
        timestamp = timestamp.replace("/", "-")
        #if(nyse.open_at_time(early, pd.Timestamp( , tz='America/New_York'))):
        # date | open | high | low | close
        col0 = timestamp #row[0]
        col1 = row[1]
        col2 = row[2]
        col3 = row[3]
        col4 = row[4]


        stockindexing.append(col0)
        stocks.append([col0,col1,col2,col3,col4])

    #ok well now we create labels... for this thing.

    y = [] #the length of tweets,

    for s in range(len(tweets)):
        thedate = tweets[s][0]
        #first, extract the date from tweets.
        #then find the index of that date in stockindexing.
        index = stockindexing.index(thedate)

        #then, do stocks[index][4]-stocks[index+1][1]
        #
        if(( float(stocks[index][4])- float(stocks[index+1][1]) ) < 0 ):
            y.append(1)

        else:
            y.append(0)


    #print(y[0])
    #print(y[1])
    #print(y[2])

    x=[]

    for t in range(len(tweets)):

        #print(type(tweets[t][0]))
        a = float(tweets[t][1])
        b = float(tweets[t][2])
        c = float(tweets[t][3])
        d = float(tweets[t][4])
        #e= time.datetime(tweets[t][0])- time.datetime(2012,1,1)
        #f= int(e.days())
        '''
        e = arrow.get(tweets[t][0])
        f = arrow.get('2012-11-15')
        print(e)
        delta = str(e-f)

        somelist = re.findall(r'\d+', delta)
        somelistindexone[0]
'''
        x.append([a,b,c,d])
        #col0 = date.isoformat()
        #col1 = row[1]
        #col2 = row[2]
        #col3 = row[3]
        #col4 = row[4]

model = Sequential()
model.add(Dense(32, input_shape=(4,), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
#model.add(Dense(256, activation='relu'))
#model.add(Dense(64, activation='relu'))

model.add(Dense(1, activation='sigmoid'))
X = np.array(x)
Y = np.array(y)
                # compile model
model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['acc'])
model.fit(X,Y, epochs=1, batch_size = 100)

sum=0
for qwer in range(len(y)):
    if y[qwer]==1:
        sum=sum+1

print(sum/len(y))
