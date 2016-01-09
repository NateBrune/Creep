import requests
import socket
from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader('templates'))
nips = []


def scan_ip(ip):
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
    parser = argparse.ArgumentParser(description='Crawl nodeinfo files')
    parser.add_argument('--out', type=str, help='The file to output the HTML to',
                        default='creep.php')
    parser.add_argument('--static', type=str,
                        help="Prefix for all static resources referenced from the output file",
                        default='static')
    parser.add_argument('file', type=str, help='list of ip addresses')
    args = parser.parse_args()
    template = env.get_template('creep.html')
    nodes = []
    with open(args.file, "r") as ipsfile:
        for ip in ipsfile:
            node = scan_ip(ip)
            if node is not None:
                if 'services' in node:
                    if type(node['services']) is list or type(node['services']) is dict:
                        nodes.append(node)
    with open(args.out, 'w') as output:
        output.write(template.render(title='Creep', nodes=nodes, static=args.static))
