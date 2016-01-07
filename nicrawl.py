import requests
import sys
import socket

try:
    import dominate
    import dominate.tags
except ImportError:
    print('dominate is required')
    print('https://github.com/Knio/dominate')
    sys.exit(0)

doc = dominate.document(title='creep')
nips = []


def scan_ips(ip):
    try:
        webFile = requests.get('http://['+ip.rstrip()+']/nodeinfo.json', timeout=3).json()
        with doc:
            dominate.tags.a('http://['+ip.rstrip()+']/nodeinfo.json',
                            href='http://['+ip.rstrip()+']/nodeinfo.json')
            dominate.tagsh4('Node')
            with dominate.tags.dl():
                dominate.tags.dt('IP')
                dominate.tags.dd(str(ip.rstrip()))
                for key in webFile:
                    if type(webFile[key]) is not list and type(webFile[key]) is not dict:
                        if str(key) != "ip":
                            dominate.tags.dt(str(key))
                            dominate.tags.dd(webFile[key])
                            print(webFile[key])

            if "contact" in webFile:
                if type(webFile['contact']) is list or type(webFile['contact']) is dict:
                    dominate.tags.h4('Contact')
                    with dominate.tags.dl():
                        for key in webFile['contact']:
                            dominate.tags.dt(str(key))
                            dominate.tags.dd(webFile['contact'][key])
                            print(webFile['contact'][key])
            if "services" in webFile:
                if type(webFile['services']) is list or type(webFile['services']) is dict:
                    dominate.tags.h4('Services')
                    with dominate.tags.dl():
                        for key in webFile['services']:
                            for key2 in key:
                                dominate.tags.dt(str(key2))
                                dominate.tags.dd(key[key2])
            dominate.tags.hr('')
        f = open('creep.php', 'r+')
        f.write(str(doc))
        f.close()
    except requests.exceptions.Timeout as ex:
        print(str(ip.rstrip()) + " connection timed out")
    except socket.timeout as ex:
        print(str(ip.rstrip()) + " connection timed out")
    except ValueError as ex:
        print(str(ip.rstrip()) + " does not have a valid nodeinfo.json")
        nips.append(ip.rstrip())
    except AttributeError as ex:
        print(str(ip.rstrip()) + " AttributeError")
    except requests.exceptions.RequestException as ex:
        print("A requests exception occured! %s" % ex)


if __name__ == '__main__':
    # Process command line options
    import argparse
    parser = argparse.ArgumentParser(description='Crawl nodeinfo files')
    parser.add_argument('file', type=str, help='list of ip addresses')
    args = parser.parse_args()
    with doc.head:
        dominate.tags.link(rel='stylesheet', href='creepstyle.css')

    with doc:
        dominate.tags.h1('Creep')
        dominate.tags.p('Rendering of nodeinfo.json data. Maintained by NAT.')
        dominate.tags.p("""nodeinfo.json is an identification convention for cjdns nodes to provide
        info about themselves. This page aggregates nodeinfo.json data found online, to help you
        discover services on Hyperboria and see who operates them.""")
        dominate.tags.p('Without further ado...')
        dominate.tags.hr('')
    try:
        with open(args.file, "r") as ipsfile:
            for ips in ipsfile:
                scan_ips(ips)
    except KeyboardInterrupt as ex:
        sys.exit(0)
    with doc:
        print("Writing Honorable Mentions")  # literally doesnt work
        dominate.tags.hr('')   # but guess how much I care...
        dominate.tags.h4('Honorable Mentions')
        outfile = open('creep.php', 'r+')
        outfile.write(str(doc))
        for ip in enumerate(nips):
            strings = str(ip) + ' invalid json file.'  # i care a little bit
            dominate.tags.p(str(strings))
            print(ip)
            outfile.write(str(doc))
        outfile.close()  # but I dont care at all.
