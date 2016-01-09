#!/usr/bin/env python
try:
    import queue
except ImportError:
    import Queue as queue
import time
import threading
import requests
import sys

USER_AGENT = "NAT's Creep nodeinfo.json scanner +https://github.com/NateBrune/Creep"

# Various settings
numthreads = 300
resultList = []
wq = queue.Queue()


# Thread Launcher
def launchThreads(numthreads):
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
            ret = requests.get('http://['+str(ip)+']/nodeinfo.json', allow_redirects=False,
                               timeout=2, headers={'User-Agent': USER_AGENT})
            if ret.status_code == 200:
                print("%s/nodeinfo.json Exists!" % (ip))
                try:
                    f = open('nis.log', 'a+')
                    f.write(str(ip) + "\n")
                    f.close()
                except all as ex:
                    print(str(ex))
                pass
            else:
                pass
        except:
            pass
    return

if __name__ == '__main__':
    # Process command line options
    import argparse
    parser = argparse.ArgumentParser(description='Scan IPv6 file for nodeinfo.json files')
    parser.add_argument('file', type=str, help='list of ip addresses')
    args = parser.parse_args()

    # Run scans, die properly on CTRL-C
    try:
        launchThreads(numthreads)
    except KeyboardInterrupt as ex:
        sys.exit(0)
