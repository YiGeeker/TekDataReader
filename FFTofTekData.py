"""FFT of the Tektronix oscilloscope data."""

# !python
# -*- coding: utf-8 -*-
# Data: 2017.12.08
# Version: 1.0

import csv
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib import ticker

keyWords = ('Horizontal Units', 'Horizontal Scale', 'Sample Interval', 'Record Length', 'Vertical Units', 'Vertical Offset', 'Vertical Scale', 'TIME')
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

# Draw the whole plot
fig, ax = plt.subplots()
for num in range(0, channelNum):
    plt.plot(t, scaleValue[num], label = keyDict['TIME'][num]+', '+'Unit = '+keyDict['Vertical Units'][num]+', '+'Scale = '+keyDict['Vertical Scale'][num])

titleText = keyDict['Record Length'][0]+' Points of '+str(keyDict['TIME'][0])
for num in range(1, channelNum):
    titleText += ', '+str(keyDict['TIME'][num])

plt.title(titleText)
plt.xlabel('Time: '+keyDict['Horizontal Units'][0])
plt.ylabel('Value')
ax.xaxis.set_major_locator(ticker.MultipleLocator(float(keyDict['Horizontal Scale'][0])))
axFormatter = ticker.ScalarFormatter(useMathText=True)
axFormatter.set_scientific(True)
axFormatter.set_powerlimits((-1, 2))
ax.xaxis.set_major_formatter(axFormatter)
ax.yaxis.set_major_formatter(axFormatter)
plt.grid(b=True, linestyle='dotted')
plt.legend(loc='best')

# Draw each channel raw data and the FFT
for num in range(0, channelNum):
    plt.figure(num=num+2, figsize=(6.5, 12))
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312)
    ax3 = plt.subplot(313)
    
    plt.sca(ax1)
    plt.plot(t, rawValue[num])

    titleText = keyDict['Record Length'][0]+' Points of '+str(keyDict['TIME'][num])
    plt.title(titleText)
    plt.xlabel('Time: '+keyDict['Horizontal Units'][0])
    plt.ylabel('Value')
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(float(keyDict['Horizontal Scale'][0])))
    ax1.xaxis.set_major_formatter(axFormatter)
    ax1.yaxis.set_major_formatter(axFormatter)
    plt.grid(b=True, linestyle='dotted')

    length = len(rawValue[num])
    samplingRate = 1/float(keyDict['Sample Interval'][0])
    fftValue = np.fft.rfft(rawValue[num])/length
    freqs = np.linspace(0, samplingRate/2, length/2+1)
    index = np.arange(0, length, 1.0)/length*2*np.pi

    plt.sca(ax2)
    plt.plot(freqs, np.abs(fftValue))

    # titleText = 'FFT Absolute Value of '+str(keyDict['TIME'][num])
    # plt.title(titleText)
    plt.xlabel('Frequence(Hz)')
    plt.ylabel('Absolute Value')
    # ax2.xaxis.set_major_locator(ticker.MultipleLocator(np.pi/4))
    ax2.xaxis.set_major_formatter(axFormatter)
    ax2.yaxis.set_major_formatter(axFormatter)
    plt.grid(b=True, linestyle='dotted')
    
    plt.sca(ax3)
    plt.plot(freqs, np.rad2deg(np.angle(fftValue)))
    
    # titleText = 'FFT Angle of '+str(keyDict['TIME'][num])
    # plt.title(titleText)
    plt.xlabel('Frequence(Hz)')
    plt.ylabel('Angle($^\circ$)')
    # ax3.xaxis.set_major_locator(ticker.MultipleLocator(np.pi/4))
    ax3.xaxis.set_major_formatter(axFormatter)
    ax3.yaxis.set_major_formatter(axFormatter)
    plt.grid(b=True, linestyle='dotted')
    
plt.show()
