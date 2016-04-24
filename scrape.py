from bs4 import BeautifulSoup
import requests

import logging
import os
import re
import sys
from urlparse import urlparse


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

PREAMBLE = re.compile(
    r'\A.*<!-- text above generated by server\. PLEASE REMOVE -->',
    flags=re.DOTALL)

POSTAMBLE = re.compile(
    r'<!-- text below generated by server. PLEASE REMOVE -->.*\Z',
    flags=re.DOTALL)

MIDAMBLE = re.compile(
    r'<!-- following code added by server\. PLEASE REMOVE -->.*<!-- preceding code added by server\. PLEASE REMOVE -->',
    flags=re.DOTALL)


def scrape(urls, overwrite=False):
    for url in urls:
        scrape_url(url, overwrite=overwrite)


def scrape_url(url, overwrite=False):
    log.info("Scraping {}".format(url))
    url_components = urlparse(url)

    path_components = list(os.path.split(url_components.path))
    path_components[0] = re.sub(r'^/+', '', path_components[0])
    if '.' not in path_components[-1]:
        path_components[-1] = 'index.html'

    path = os.path.join(*path_components)
    destination = os.path.join(url_components.netloc, path)

    if os.path.exists(destination):
        if overwrite:
            log.debug("Overwriting {}".format(destination))
        else:
            log.debug("{} already exists - skipping".format(destination))
            return
    else:
        log.debug("Creating {}".format(destination))

    destination_dir = os.path.dirname(destination)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    response = requests.get(url)
    if response.status_code >= 400:
        log.info("Got {} - skipping".format(response.status_code))
        return

    html = response.content
    html = remove_additions(html)
    html = rewrite_embeds(html, path)

    with open(destination, 'wb') as f:
        f.write(html)


def rewrite_embeds(html, path):
    soup = BeautifulSoup(html, "lxml")

    for tag in soup.find_all('img'):
        try:
            if hasattr(tag, 'attrs') \
               and 'src' in tag.attrs \
               and not tag.attrs['src'].startswith('http'):
                src = tag.attrs['src'].decode('utf-8', 'replace')
                src = os.path.join(os.path.dirname(path), src)
                if not src.startswith('/'):
                    src = '/' + src
                src = u"http://www.oocities.org{}".format(src).encode('utf-8', 'replace')

                log.debug(" -> Rewriting {} to {}".format(repr(tag.attrs['src']), repr(src)))
                tag.attrs['src'] = src
        except UnicodeEncodeError, UnicodeDecodeError:
            pass

    return str(soup)


def remove_additions(html):
    if PREAMBLE.search(html):
        log.debug(" -> Removing preamble")
        html = PREAMBLE.sub('', html)
    else:
        log.debug(" -> No preamble found")

    if POSTAMBLE.search(html):
        log.debug(" -> Removing postamble")
        html = POSTAMBLE.sub('', html)
    else:
        log.debug(" -> No postamble found")

    if MIDAMBLE.search(html):
        log.debug(" -> Removing midamble")
        html = MIDAMBLE.sub('', html)
    else:
        log.debug(" -> No midamble found")

    return html


if __name__ == '__main__':
    urls = [u.strip() for u in sys.stdin.readlines()]
    scrape(urls, overwrite=False)