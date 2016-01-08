import requests
import sys
import socket
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
nips = []


def scan_ips(ip):
    try:
        return requests.get('http://['+ip.rstrip()+']/nodeinfo.json', timeout=3).json()
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
    import json
    parser = argparse.ArgumentParser(description='Crawl nodeinfo files')
    parser.add_argument('file', type=str, help='list of ip addresses')
    args = parser.parse_args()
    template = env.get_template('creep.html')
    nodes = []
    with open(args.file, "r") as ipsfile:
        for ips in ipsfile:
            node = scan_ips(ips)
            if node is not None:
                nodes.append(node)
    # print(json.dumps(nodes))
    with open('creep.php', 'w') as output:
        output.write(template.render(title='Creep', nodes=nodes))
