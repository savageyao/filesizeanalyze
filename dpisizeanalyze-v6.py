# -*- coding: utf-8 -*-
# yao.savage@gmail.com
# awk -F '/' '{print $5}' 4G20160204 | sort > 4Gnode
# check file size and gen file size graph
# DONE(savage) plot total file size 20160215 done by function plotgraph()
# DONE(savage) plot certain node file size 20160215 done by function plot4graph plot3graph

import datetime
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from pandas import DataFrame


def timeprocessing(year, month, day, hour, minute, second):
    # make sure time minute is even range(0,59,2)
    if minute in range(1, 61, 2):
        return datetime.datetime(year, month, day, hour, minute) + datetime.timedelta(
            seconds=60)
    else:
        return datetime.datetime(year, month, day, hour, minute)


def getfilename(inurl):
    # sample:
    # /media/data1/4g_3rdpartyflow/3rdpartyflow_20160125_085200_001073.log
    return inurl.split('/')[-1]


def getfiletime(infilename):
    # sample:
    # 3rdpartyflow_20160125_085200_001073.log
    YYYYMMDD = infilename.split('_')[1]
    year = int(YYYYMMDD[0:4])
    month = int(YYYYMMDD[4:6])
    day = int(YYYYMMDD[6::])
    HHMMSS = infilename.split('_')[2]
    hour = int(HHMMSS[0:2])
    minute = int(HHMMSS[2:4])
    second = int(HHMMSS[4::])
    return timeprocessing(year, month, day, hour, minute, second)
    # return datetime.datetime(year, month, day, hour, minute,second )


def gethostnode(infilename):
    # sample:
    # /media/data/3rdpartyflow/3rdpartyflow_20160126_081400_001010.log
    # /media/data/4g_3rdpartyflow/3rdpartyflow_20160126_000200_001022.log
    # a = infilename.split('/')[4]
    # b = a.split('_')[-1]
    # c = b.split('.')[0]
    # nodename = infilename.split('/')[4].split('_')[-1].split('.')[0]
    nodename = infilename.split('_')[-1].split('.')[0]
    return nodename


def gettimeline(in3g, in4g):
    startlist = []
    endlist = []
    for x in in3g:
        timeline = sorted(x.keys())
        if len(timeline) > 0:
            startlist.append(timeline[0])
            endlist.append(timeline[-1])
    for x in in4g:
        timeline = sorted(x.keys())
        if len(timeline) > 0:
            startlist.append(timeline[0])
            endlist.append(timeline[-1])
    starttime = sorted(startlist)[0]
    endtime = sorted(endlist)[-1]
    # print starttime,endtime
    # print type(starttime),type(endtime)
    # return datetime.datetime object
    return starttime, endtime


def gendf(intimeline, indict):
    # fnpd = DataFrame(indict).reindex(index=intimeline,fill_value=0)
    # fill null with zero
    fnpd = DataFrame(indict).reindex(index=intimeline).fillna(0)
    # fnpd.fillna(value=0)
    # fnpd = DataFrame(indict)
    # i=1
    # for everydict in inlist:
    #     # print type(x)
    #     # print eval(everydict)
    #     fnpd.ix[i] = reindex(intimeline,everydict)
    #     i+=1
    #     # print fnpd
    return fnpd


def checkmissing(intimeline1, inpd3g, inpd4g):
    # DONE(savage) check size 0 file with pd. 20160216
    # node3G = set(['001002', '001010', '001019', '001020', '001041', '001044'])
    # node4G = set(['001022', '001052', '001053', '001054', '001055', '001073'])
    # node3G = Series(['001002', '001010', '001019', '001020', '001041', '001044'])
    # node4G = Series(['001022', '001052', '001053', '001054', '001055', '001073'])
    dictnode3G = {'node02': '001002', 'node10': '001010', 'node19': '001019', 'node20': '001020', 'node41': '001041',
                  'node44': '001044',}
    dictnode4G = {'node22': '001022', 'node52': '001052', 'node53': '001053', 'node54': '001054', 'node55': '001055',
                  'node73': '001073',}
    print '-' * 12, 'checking 3G xdr', '-' * 12
    for index, row in inpd3g.iterrows():
        if True not in list(inpd3g.ix[index, :].isin([0])):
            continue
        else:
            # print index, list(row[row==0].index)
            # print index.strftime(format='%Y-%m-%d %H:%M'), list(row[row==0].index)
            print index.strftime(format='%Y-%m-%d %H:%M'), '3G xdr missing:',
            a = list(row[row == 0].index)
            for x in a:
                print dictnode3G[x],
            print ''
    print '-' * 12, 'checking 4G xdr', '-' * 12
    for index, row in inpd4g.iterrows():
        if True not in list(inpd4g.ix[index, :].isin([0])):
            continue
        else:
            print index.strftime(format='%Y-%m-%d %H:%M'), '4G xdr missing:',
            a = list(row[row == 0].index)
            for x in a:
                print dictnode4G[x],
            print ''
    return 0


def gentimeline(starttime, endtime):
    # timeline = [endtime - starttimedatetime.timedelta(days=x) for x in range(0, numdays)]
    # print endtime -starttime
    # print type(endtime -starttime)
    # timeline = (endtime -starttime).total_seconds()/120
    number = (endtime - starttime).total_seconds() / 120
    # print number
    timeline = []
    for x in range(0, int(number) + 1):
        timeline.append(starttime + datetime.timedelta(minutes=2 * x))
    # print timeline
    # index = pd.datetime('2000-1-1', periods=1000, freq='M')
    return timeline


def plot4ggraph(pd4g):
    formatter = DateFormatter('%m-%d\n%H:%M')
    plt.figure('4G file size')
    # plt.plot_date(pd4g.index, pd4g['node22'] / (1024 * 1024), 'b', xdate=True, ydate=False, label='node22')
    plt.plot_date(pd4g.index, pd4g['node52'] / (1024 * 1024), 'g', xdate=True, ydate=False, label='node52')
    plt.plot_date(pd4g.index, pd4g['node53'] / (1024 * 1024), 'r', xdate=True, ydate=False, label='node53')
    # plt.plot_date(pd4g.index, pd4g['node54'] / (1024 * 1024), 'c', xdate=True, ydate=False, label='node54')
    plt.plot_date(pd4g.index, pd4g['node55'] / (1024 * 1024), 'm', xdate=True, ydate=False, label='node55')
    plt.plot_date(pd4g.index, pd4g['node73'] / (1024 * 1024), 'y', xdate=True, ydate=False, label='node73')
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.title('4G file size')
    plt.ylabel('file size(MB)')
    plt.legend(loc='upper left')
    plt.show()


def plot3ggraph(pd3g):
    formatter = DateFormatter('%m-%d\n%H:%M')
    plt.figure('3G file size')
    plt.plot_date(pd3g.index, pd3g['node02'] / (1024 * 1024), 'b', xdate=True, ydate=False, label='node02')
    plt.plot_date(pd3g.index, pd3g['node10'] / (1024 * 1024), 'g', xdate=True, ydate=False, label='node10')
    plt.plot_date(pd3g.index, pd3g['node19'] / (1024 * 1024), 'r', xdate=True, ydate=False, label='node19')
    plt.plot_date(pd3g.index, pd3g['node20'] / (1024 * 1024), 'c', xdate=True, ydate=False, label='node20')
    plt.plot_date(pd3g.index, pd3g['node41'] / (1024 * 1024), 'm', xdate=True, ydate=False, label='node41')
    plt.plot_date(pd3g.index, pd3g['node44'] / (1024 * 1024), 'y', xdate=True, ydate=False, label='node44')
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.title('3G file size')
    plt.ylabel('file size(MB)')
    plt.legend(loc='upper left')
    plt.show()


def sumsize(inpd):
    # print inpd.ix[::,0]+inpd.ix[::,1]+inpd.ix[::,2]+inpd.ix[::,3]+inpd.ix[::,4]+inpd.ix[::,5]
    # col = inpd.columns
    # index1 = inpd.index
    return inpd.sum(axis=1)
    # print inpd.ix[::,6]
    # return inpd.ix[::,0]+inpd.ix[::,1]+inpd.ix[::,2]+inpd.ix[::,3]+inpd.ix[::,4]+inpd.ix[::,5]


def plotgraph(pd3g, pd4g):
    # timeline3g= sorted(list(pd3g.index.values))
    # timeline4g= sorted(list(pd4g.index.values))
    if list(pd3g.index.values) == list(pd4g.index.values):
        print 'num and size timeline is same'
    else:
        print 'num and size timeline is NOT same'
    total3g = pd3g.sum(axis=1).sum(axis=0) / (1024.0 ** 3)
    total4g = pd4g.sum(axis=1).sum(axis=0) / (1024.0 ** 3)
    print '3G    size:', format(total3g, '.4g'), 'GByte'
    print '4G    size:', format(total4g, '.4g'), 'GByte'
    print 'Total size:', format(total3g + total4g, '.4g'), 'GByte'
    formatter = DateFormatter('%m-%d\n%H:%M')
    plt.figure('DPI file size')
    # plt.plot_date(timeline3g, sumsize(pd3g)/(1024*1024), 'g', xdate=True, ydate=False, label='3G')
    # plt.plot_date(timeline4g, sumsize(pd4g)/(1024*1024), 'b', xdate=True, ydate=False, label='4G')
    plt.plot_date(pd3g.index, sumsize(pd3g) / (1024 * 1024), 'g', xdate=True, ydate=False, label='3G')
    plt.plot_date(pd4g.index, sumsize(pd4g) / (1024 * 1024), 'b', xdate=True, ydate=False, label='4G')
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.title('DPI file size')
    plt.ylabel('file size(MB)')
    plt.legend(('3G', '4G'), loc='upper left')
    plt.show()


def checkdelta(inpd, indict):
    # DONE(savage) check file size decending
    diff1pd = inpd.diff(1)
    shift1pd = inpd.shift(1)
    pcentpd = diff1pd / shift1pd
    print '-' * 12, 'checking delta', '-' * 12
    # pcentpd.groupby(pcentpd)
    for index, row in pcentpd.iterrows():
        # if True not in list(abs(pcentpd.ix[index, :]) > 0.5):
        # print type(pcentpd.ix[index, :])
        # print pcentpd.ix[index, :]
        # if pcentpd.ix[index, :] in range :
        #     print pcentpd.ix[index, :]
        #     print pcentpd.ix[index, :]
        # print pcentpd.ix[index, :].any
        # print type(pcentpd.ix[index, :].all >-0.6)
        if True not in list(pcentpd.ix[index, :] < -0.2):
            # print pcentpd.ix[index, :] < -0.5
            continue
        else:
            print index.strftime(format='%Y-%m-%d %H:%M'), 'delta < -20%:',
            # a = list(row[abs(row) >0.5].index)
            a = list(row[row < -0.2].index)
            for x in a:
                print indict[x],
            print ''


def dataprocess(infile):
    filehandle = open(infile, 'r')
    rawdata = filehandle.readlines()
    filehandle.close()
    node02 = defaultdict(int)
    node10 = defaultdict(int)
    node19 = defaultdict(int)
    node20 = defaultdict(int)
    node41 = defaultdict(int)
    node44 = defaultdict(int)
    node22 = defaultdict(int)
    node52 = defaultdict(int)
    node53 = defaultdict(int)
    node54 = defaultdict(int)
    node55 = defaultdict(int)
    node73 = defaultdict(int)
    for everyline in rawdata:
        # skip linux command line or empty line
        if 'linux-e9yv' in everyline or 'You have new mail' in everyline or len(everyline.strip()) == 0:
            continue
            # print x
        else:
            # sample:
            # /media/data1/4g_3rdpartyflow/3rdpartyflow_20160203_102600_001073.log 522283835
            # split fileurl and size
            fileurl, size = everyline.split()
            filename = getfilename(fileurl)
            timeline = getfiletime(filename)
            hostnode = gethostnode(filename)
            if '4g_' in fileurl:
                my4gdict = {
                    '001022': node22,
                    '001052': node52,
                    '001053': node53,
                    '001054': node54,
                    '001055': node55,
                    '001073': node73,
                }.get(hostnode)
                my4gdict[timeline] += int(size)
            else:
                my3gdict = {
                    '001002': node02,
                    '001010': node10,
                    '001019': node19,
                    '001020': node20,
                    '001041': node41,
                    '001044': node44,
                }.get(hostnode)
                my3gdict[timeline] += int(size)
    node4gsize = {'node22': node22, 'node52': node52, 'node53': node53, 'node54': node54, 'node55': node55,
                  'node73': node73}
    node3gsize = {'node02': node02, 'node10': node10, 'node19': node19, 'node20': node20, 'node41': node41,
                  'node44': node44}
    starttime, endtime = gettimeline([node02, node10, node19, node20, node41, node44],
                                     [node22, node52, node53, node54, node55, node73])
    newtimeline = gentimeline(starttime, endtime)
    pd3g = gendf(newtimeline, node3gsize)
    pd4g = gendf(newtimeline, node4gsize)
    # print type(list(pd3g.index.values))
    prefix = starttime.strftime('%Y%m%d')
    # pd3g.to_csv('logfile/'+prefix+'-pd3g.csv')
    # pd4g.to_csv('logfile/'+prefix+'-pd4g.csv')
    return starttime, endtime, pd3g, pd4g


inputfile = 'logfile/20160225.log'
starttime, endtime, pd3g, pd4g = dataprocess(inputfile)
# node3G = set(['001002', '001010', '001019', '001020', '001041', '001044'])
# node4G = set(['001022', '001052', '001053', '001054', '001055', '001073'])
dictnode3G = {'node02': '001002', 'node10': '001010', 'node19': '001019', 'node20': '001020', 'node41': '001041',
              'node44': '001044',}
dictnode4G = {'node22': '001022', 'node52': '001052', 'node53': '001053', 'node54': '001054', 'node55': '001055',
              'node73': '001073',}
# prefix = starttime.strftime('%Y%m%d')
# sumsize(pd4g)

timeline1 = gentimeline(starttime, endtime)
checkmissing(timeline1, pd3g, pd4g)
plotgraph(pd3g, pd4g)
plot3ggraph(pd3g)
plot4ggraph(pd4g)
checkdelta(pd3g, dictnode3G)
checkdelta(pd4g, dictnode4G)
