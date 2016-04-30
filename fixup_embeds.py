import logging
import os
import random
import re
import sys

import requests


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.propagate = False

ARCHIVE_ORG = 'http://web.archive.org/web/http://www.geocities.com/'
OOCITIES = 'http://www.oocities.org/'

SRC = re.compile(r'\b(src|background)\s*=\s*(".*?"|\'.*?\')')
URL_PREFIX = OOCITIES

MIRRORS = [
    ARCHIVE_ORG,
    'http://geocities.ws/',
    'http://reocities.com/',
]


def replace(match):
    tag_name = match.group(1)
    value = match.group(2)
    quote_char = value[0]
    src = value[1:-1]

    if not src.startswith(URL_PREFIX):
        return match.group(0)

    path = src.replace(URL_PREFIX, '', 1)
    replacement = None

    for mirror in random.sample(MIRRORS, len(MIRRORS)):
        url = mirror + path

        try:
            response = requests.head(url, allow_redirects=True)
        except Exception:
            continue

        if 200 <= response.status_code < 300:
            replacement = response.url
            break

    if not replacement:
        log.debug(" -> No working URL found for {}".format(path))
        replacement = ARCHIVE_ORG + path  # in the hope it comes online someday...?

    replacement = "{}={}{}{}".format(tag_name, quote_char, replacement, quote_char)
    log.debug(" -> Rewriting {} to {}".format(match.group(0), replacement))
    return replacement


html = sys.stdin.read()
html = SRC.sub(replace, html)
sys.stdout.write(html)
