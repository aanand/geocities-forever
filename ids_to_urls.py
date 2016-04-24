import logging
import re
import sys


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

with open('assets.txt', 'rb') as f:
    assets = [line.strip() for line in f.readlines()]

def replace_id(match):
    attr = match.group(1).lower()
    if attr == 'bg':
        attr = 'background'

    group = match.group(2)
    quote_char = group[0]
    asset_id = int(group[1:-1])
    log.debug(asset_id)

    if asset_id >= len(assets):
        log.debug("Asset #{} not found".format(asset_id))
        return match.group(0)

    url = assets[asset_id]
    return '{}={}{}{}'.format(attr, quote_char, url, quote_char)

html = re.sub(
    r'\b(src|bg)\s*=\s*("\d+"|\'\d+\')',
    replace_id,
    sys.stdin.read(),
    flags=re.IGNORECASE,
)

print(html)
