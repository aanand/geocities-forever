from bs4 import BeautifulSoup

import logging
import os
import sys


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


in_dir = sys.argv[1]
out_dir = sys.argv[2]


def rewrite_embeds_file(from_path, to_path, site_name):
    with open(from_path, 'rb') as f:
        with open(to_path, 'wb') as t:
            t.write(rewrite_embeds_string(f.read(), site_name))


def rewrite_embeds_string(html, site_name):
    soup = BeautifulSoup(html, "lxml")

    for tag in soup.find_all('img'):
        try:
            if hasattr(tag, 'attrs') \
               and 'src' in tag.attrs \
               and not tag.attrs['src'].startswith('http'):
                src = tag.attrs['src'].decode('utf-8', 'replace')
                src = os.path.join('/', site_name, src)
                if not src.startswith('/'):
                    src = '/' + src
                src = u"http://www.oocities.org{}".format(src).encode('utf-8', 'replace')

                log.debug(" -> Rewriting {} to {}".format(repr(tag.attrs['src']), repr(src)))
                tag.attrs['src'] = src
        except UnicodeEncodeError, UnicodeDecodeError:
            pass

    return str(soup)


for site_name in os.listdir(in_dir):
    site_path = os.path.join(in_dir, site_name)

    if os.path.isdir(site_path):
        for file_name in os.listdir(site_path):
            file_path = os.path.join(site_path, file_name)

            if os.path.isfile(file_path):
                destination_dir = os.path.join(out_dir, site_name)
                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                destination = os.path.join(destination_dir, file_name)
                log.debug("({}) {} -> {}".format(site_name, file_path, destination))

                rewrite_embeds_file(file_path, destination, site_name)
