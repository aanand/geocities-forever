import logging
import re
import sys


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

assets = []

def replace_url(match):
    attr = match.group(1).lower()
    if attr == 'background':
        attr = 'bg'

    group = match.group(2)
    quote_char = group[0]
    url = group[1:-1]
    log.debug(url)

    try:
        index = assets.index(url)
    except ValueError:
        assets.append(url)
        index = len(assets) - 1

    return '{}={}{}{}'.format(attr, quote_char, index, quote_char)

html = re.sub(
    r'\b(src|background)\s*=\s*(".*?"|\'.*?\')',
    replace_url,
    sys.stdin.read(),
    flags=re.IGNORECASE,
)

print(html)

with open('assets.txt', 'wb') as f:
    for url in assets:
        f.write(url + '\n')
