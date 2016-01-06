#!/usr/bin/env python
import os
import sys
import Queue
import time
import threading
import urllib2

# Various settings
numthreads = 150
resultList = []
wq = Queue.Queue()

# Thread Launcher
def launchThreads(argsfile,numthreads):
    global wq
    # Enqueing Stuff
    with open(args.file, "r") as ipsfile:
      for ip in ipsfile:
        wq.put(ip)
    # Spawning Threads
    for i in range(numthreads):
        t = threading.Thread(target=tRun)
        t.start()
    while threading.active_count() > 1:
        time.sleep(0.1)

# Thread
def tRun():
    global wq
    global resultList
    while not wq.empty():
        ip = wq.get().rstrip()
        #print str(ip)
        try:
            ret = urllib2.urlopen('http://['+str(ip)+']/nodeinfo.json')
            if ret.code == 200:
                print "%s/nodeinfo.json Exists!" % (ip)
                resultList.append('%s' % (ip))
                pass
            else:
                #print "%s/nodeinfo.json 404" % (ip)
                pass
        except:
            #print "%s/nodeinfo.json 404" % (ip)
            pass

if __name__ == '__main__':
    # Process command line options
    import argparse
    parser = argparse.ArgumentParser(description = 'Scan IPv6 file for nodeinfo.json files')
    parser.add_argument('file', type = str, help = 'list of ip addresses')
    args = parser.parse_args()

    # Run scans, die properly on CTRL-C
    try:
      launchThreads(args.file,numthreads)

      # Print results
      print 'Final result list'
      for x in resultList:
         print x
      print "Number of open resolvers: %s" %(len(resultList))

    except KeyboardInterrupt, ex:
        pass
