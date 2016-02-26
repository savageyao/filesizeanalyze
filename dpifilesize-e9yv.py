#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime
import os


def getvalidfile(myday, inlist, inpath):
    outfilelist = []
    for everyfile in inlist:
        if '_' + myday + '_' in everyfile and (everyfile.endswith('.log') or everyfile.endswith('.gz')):
            outfilelist.append(inpath + everyfile)
    return outfilelist


def getfilesize(inlist):
    outfilesize = {}
    for eachfile in inlist:
        outfilesize[eachfile] = os.stat(eachfile).st_size
    return outfilesize


def getfileinfo(myday, inpath):
    os.chdir(inpath)
    allfilelist = os.listdir(inpath)
    validfile = getvalidfile(myday, allfilelist, inpath)
    print inpath, 'total', len(validfile), 'file'
    datasize = getfilesize(validfile)
    return sorted(validfile), datasize


def file3gsize(bigday):
    print "begin check 3G file size at", str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    path3g = '/media/data/3rdpartyflow/'
    dayfile, datasize = getfileinfo(bigday, path3g)
    path3g1 = '/media/data1/3rdpartyflow/'
    dayfile1, datasize1 = getfileinfo(bigday, path3g1)
    file3g = dayfile + dayfile1
    size3g = dict(datasize, **datasize1)
    print "finish check 3G file size at", str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return file3g, size3g


def file4gsize(bigday):
    print "begin check 4G file size at", str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    path4g = '/media/data/4g_3rdpartyflow/'
    dayfile, datasize = getfileinfo(bigday, path4g)
    path4g1 = '/media/data1/4g_3rdpartyflow/'
    dayfile1, datasize1 = getfileinfo(bigday, path4g1)
    file4g = dayfile + dayfile1
    size4g = dict(datasize, **datasize1)
    print "finish check 4G file size at", str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return file4g, size4g


print "Job bengin", str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')
# yesterday = '20160225'
file3g, size3g = file3gsize(yesterday)
file4g, size4g = file4gsize(yesterday)

os.chdir('/root/script')
filename = yesterday + '-SIZE' + '.log'
outputfile = open(filename.decode('utf-8'), "w")
for x in file3g:
    print >> outputfile, x, size3g[x]
for x in file4g:
    print >> outputfile, x, size4g[x]
outputfile.close()
print "Job done", str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
