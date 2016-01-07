import requests
import sys
import json
import socket
import re

try:
    import dominate
    from dominate.tags import *
except:
    print('dominate is required')
    print('https://github.com/Knio/dominate')
    sys.exit(0)

doc = dominate.document(title='creep')
nips = []

def scan_ips(ip):
    try:
        webFile = requests.get('http://['+ip.rstrip()+']/nodeinfo.json', timeout=3).json()
        with doc:
            a('http://['+ip.rstrip()+']/nodeinfo.json', href='http://['+ip.rstrip()+']/nodeinfo.json')
            h4('Node')
            with dl():
                dt('IP')
                dd(str(ip.rstrip()))
                for key in webFile:
                    if type(webFile[key]) is not list and type(webFile[key]) is not dict:
                        if str(key) != "ip":
                            dt(str(key))
                            dd(webFile[key])
                            print(webFile[key])

            if webFile.has_key('contact'): #I am better at getting phone numbers in cyber-space than I am irl...
                if type(webFile['contact']) is list or type(webFile['contact']) is dict:
                    h4('Contact')
                    with dl():
                        for key in webFile['contact']:
                            dt(str(key))
                            dd(webFile['contact'][key])
                            print(webFile['contact'][key])
            if webFile.has_key('services'):
                try:
                    if type(webFile['services']) is list or type(webFile['services']) is dict:
                        h4('Services')
                        with dl():
                            for key in webFile['services']:
                                for key2 in key:
                                    dt(str(key2))
                                    dd(key[key2])
                except:
                    pass #meh
            hr('')
        f = open('creep.php', 'r+')
        f.write(str(doc))
        f.close()
    except requests.exceptions.Timeout as ex:
        print(str(ip.rstrip()) + " connection timed out")
        pass
    except socket.timeout as ex:
        print(str(ip.rstrip()) + " connection timed out")
        pass
    except ValueError as ex:
        print(str(ip.rstrip()) + " does not have a valid nodeinfo.json")
        nips.append(ip.rstrip())
        pass
    except AttributeError as ex:
        print(str(ip.rstrip()) + " AttributeError")
        pass
    except requests.exceptions.RequestException as ex:
        print("A requests exception occured! %s" % ex)
        pass
    except all as ex:
            pass

if __name__ == '__main__':
    # Process command line options
    import argparse
    parser = argparse.ArgumentParser(description = 'Crawl nodeinfo files')
    parser.add_argument('file', type = str, help = 'list of ip addresses')
    args = parser.parse_args()
    with doc.head:
        link(rel='stylesheet', href='creepstyle.css')

    with doc:
        h1('Creep')
        p('Rendering of nodeinfo.json data. Maintained by NAT.')
        p('nodeinfo.json is an identification convention for cjdns nodes to provide info about themselves. This page aggregates nodeinfo.json data found online, to help you discover services on Hyperboria and see who operates them.')
        p('Without further ado...')
        hr('')
    try:
        with open(args.file, "r") as ipsfile:
            for ips in ipsfile:
                scan_ips(ips)
    except KeyboardInterrupt as ex:
        sys.exit(0)
    try:
        with doc:
            print("Writing Honorable Mentions") #literally doesnt work
            hr('')                             #but guess how much I care...
            h4('Honorable Mentions')
            f = open('creep.php', 'r+')
            f.write(str(doc))
            f.close()
            for i, key in enumerate(nips):
                strings = str(key) + ' invalid json file.' #i care a little bit
                p(str(strings))
                print(key)
                f = open('creep.php', 'r+') #i mean... it would be cool and all
                f.write(str(doc))
                f.close() #but I dont care at all.
    except all as ex:
        print(str(ex)) #not at all... seriously.
