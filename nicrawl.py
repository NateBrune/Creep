import requests
import socket
from jinja2 import Environment, FileSystemLoader
import logging
import os

USER_AGENT = "NAT's Creep nodeinfo.json scanner +https://github.com/NateBrune/Creep"

env = Environment(loader=FileSystemLoader('templates'))
nips = []


def scan_ip(ip, favicon_path, logger):
    headers = {
        'User-Agent': USER_AGENT,
        'Host': "[%s]" % ip
    }
    extra = {
        'ip': ip
    }
    try:
        url = "http://[%s]/nodeinfo.json" % ip
        logger.info("Requesting /nodeinfo.json", extra=extra)
        ni = requests.get(str(url), timeout=10, headers=headers, allow_redirects=False).json()
        logger.debug("Got /nodeinfo.json", extra=extra)
        ni.update({'appendedip': ip})
        return ni
    except requests.exceptions.Timeout as ex:
        logger.warn("connection timed out", extra=extra)
    except socket.timeout as ex:
        logger.warn("connection timed out", extra=extra)
    except (ValueError, AttributeError) as ex:
        logger.warn("nodeinfo.json is not valid JSON", extra=extra)
        nips.append(ip.rstrip())
    except requests.exceptions.RequestException as ex:
        logger.warn("A requests exception occured! %s", ex, extra=extra)


if __name__ == '__main__':
    # Process command line options
    import argparse
    parser = argparse.ArgumentParser(description='Crawl nodeinfo files')
    parser.add_argument('--out', type=str, help='The file to output the HTML to',
                        default='creep.html')
    parser.add_argument('--static', type=str,
                        help="Prefix for all static resources referenced from the output file",
                        default='static')
    parser.add_argument('--favicons', type=str, help='Folder to store favicons in.',
                        default='static/favicon')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument('file', type=str, help='list of ip addresses')
    args = parser.parse_args()
    logger = logging.getLogger("nodeinfo_crawler")
    logging.basicConfig(format='%(asctime)-15s %(ip)s %(message)s')
    if args.verbose:
        logger.setLevel(level=logging.DEBUG)
    if not os.path.isdir(args.favicons):
        logger.info("Creating %s to store favicons", args.favicons)
        os.makedirs(args.favicons)
    template = env.get_template('creep.html')
    nodes = []
    with open(args.file, "r") as ipsfile:
        for ip in ipsfile:
            added = False
            node = scan_ip(ip.rstrip(), args.favicons, logger)
            if node is not None:
                if 'contact' in node:
                    if 'name' in node['contact']:
                        nodes.append(node)
                        added = True
                if 'services' in node and added == False:
                    nodes.append(node)
    with open(args.out, 'w') as output:
        output.write(template.render(title='Creep', nodes=nodes, static=args.static))
