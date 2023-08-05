import matplotlib.pyplot as plt
import os
from dateutil import parser
import datetime
from random import random

start_t=parser.parse("00:00 AM") # midnight to compare start times
    
def timeToSeconds(timeVal):
    result = None
    if timeVal:
        if type(timeVal)==type(''):
            try:
                result = parser.parse(timeVal) - start_t
            except:
                raise RuntimeError("Ack! I cannot interpret this as a time:" + timeString)
        else:
            result = datetime.datetime(start_t.year, start_t.month, start_t.day, timeVal.hour, timeVal.minute, timeVal.second) - start_t
        result = result.seconds*1.0/3600
    else:
        raise RuntimeError("Sorry, I need a string to parse for a time.")
    return result

def mapColor(newDict, d, i, colorMap, gcolors):
    colorTag = d.get('color',i)
    if type(colorTag)!=type(''):
        c=colorMap.get(colorTag,None)
        if c is None:
            if gcolors:
                c = gcolors.pop()
            else:
                c='magenta'
                colorMap[colorTag]=c
    else:
        c = colorTag
    newDict.update(c = c)
    
def plotSchedule(scheds, mainLabel="Schedule"):
    plt.figure(figsize=(12,12))

    dayMap = {'M':1,'T':2,'W':3,'R':4,'F':5}
    gcolors = ['red','green','blue','orange','purple','cyan','yellow']
    colorMap = {}

    clDicts = []  # collection of parsed schedule objects

    for i in range(len(scheds)):
        d = scheds[i] # get the dictish thing
        newDict = {}
        newDict.update(d)
        beg_t = timeToSeconds(d.get('begin'))
        end_t = timeToSeconds(d.get('end'))
        duration = end_t - beg_t
        daycount = len(d.get('days',''))
        newDict.update(beg_t = beg_t, end_t = end_t, duration = duration, daycount = daycount)
        mapColor(newDict, d, i, colorMap, gcolors) # handle color lookup
        clDicts.append((beg_t, random(), newDict))

    clDicts.sort()
    
    currentAxis = plt.gca()
    
    plt.axis([0,6,22,7])

    for k,r,v in clDicts:
        for d in v['days']:
            xi=dayMap[d]-0.4
            xf=xi+0.8
            yi=v['beg_t']
            yf=v['end_t']
            dx=xf-xi
            dy=yf-yi
            currentAxis.add_patch(plt.Rectangle((xi,yi), dx, dy, facecolor=v['c'], alpha=0.3))
            plt.text(xi+dx/2,yi+dy/2,('\n'.join(v['labels'])),ha='center', va='center')

    plt.xticks([1,2,3,4,5],['Mon','Tue','Wed','Thu','Fri'])
    currentAxis.xaxis.set_label_position('top') 
    currentAxis.xaxis.tick_top()
    currentAxis.yaxis.grid()
    yvals=range(8,23)
    ylabs = [(start_t+datetime.timedelta(y*3600.0/86400)).strftime("%I:%M %p") for y in yvals]
    plt.yticks(yvals, ylabs)
    plt.text(3,6.3,mainLabel, ha='center', fontsize=20)

if __name__=='__main__':
    scheds = [{'begin': '08:00 AM', 'end': '08:50 AM', 'days': 'MW', 'labels':['First','Second','Third']},
              {'begin': '10:00 AM', 'end': '11:50 AM', 'days': 'TRF', 'labels':['First','Second','Third']},
              {'begin': '03:00 PM', 'end': '03:50 PM', 'days': 'MWF', 'labels':['First','Second','Third']},]

    plotSchedule(scheds)
    plt.savefig("test.png")
