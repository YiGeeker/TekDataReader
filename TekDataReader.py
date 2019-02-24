"""Read the Tektronix oscilloscope data."""

# !python
# -*- coding: utf-8 -*-
# Data: 2017.9.11
# Version: 1.0
# Useage:

import csv
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib import ticker

keyWords = ('Horizontal Units', 'Horizontal Scale', 'Record Length', 'Vertical Units', 'Vertical Offset', 'Vertical Scale', 'TIME')
keyDict = {}

fileName = input('Please enter csv file of Tektronnix oscilloscope :')
# fileName = 'TekData.csv'
fin = open(fileName, 'rt')
csvReader = csv.reader(fin)

for keyWord in keyWords:
    for row in csvReader:
        if row:
            if row[0] == keyWord:
                keyDict[keyWord] = tuple(row[1:])
                break

channelNum = len(keyDict['TIME'])
# length = int(keyDict['Record Length'][0])

t = []
rawValue = [[] for n in range(0, channelNum)]
scaleValue = [[] for n in range(0, channelNum)]

for row in csvReader:
    for num, value in enumerate(row):
        if num == 0:
            t.append(float(value))
        else:
            rawValue[num-1].append(float(value))
            scaleValue[num-1].append(float(value)/float(keyDict['Vertical Scale'][num-1])+float(keyDict['Vertical Offset'][num-1]))

fig, ax = plt.subplots()
for num in range(0, channelNum):
    plt.plot(t, scaleValue[num], label=keyDict['TIME'][num]+', '+'Unit = '+keyDict['Vertical Units'][num]+', '+'Scale = '+keyDict['Vertical Scale'][num])

titleText = keyDict['Record Length'][0]+' Points of '+str(keyDict['TIME'][0])
for num in range(1, channelNum):
    titleText += ', '+str(keyDict['TIME'][num])

plt.title(titleText)
plt.xlabel('Time: '+keyDict['Horizontal Units'][0])
plt.ylabel('Value')
ax.xaxis.set_major_locator(ticker.MultipleLocator(float(keyDict['Horizontal Scale'][0])))
axFormatter = ticker.ScalarFormatter(useMathText=True)
axFormatter.set_scientific(True)
axFormatter.set_powerlimits((-1, 1))
ax.xaxis.set_major_formatter(axFormatter)
ax.yaxis.set_major_formatter(axFormatter)
plt.grid(b=True, linestyle='dotted')
plt.legend(loc='best')
plt.show()
