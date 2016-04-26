import logging
import re
import sys


log_level = logging.DEBUG if "-v" in sys.argv else logging.INFO
logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

images = []
backgrounds = []

def replace_url(match):
    attr = match.group(1).lower()
    if attr == 'background':
        attr = 'bg'
        db = backgrounds
    else:
        db = images

    group = match.group(2)
    quote_char = group[0]
    url = group[1:-1]
    log.debug(url)

    try:
        index = db.index(url)
    except ValueError:
        db.append(url)
        index = len(db) - 1

    return '{}={}{}{}'.format(attr, quote_char, index, quote_char)

def save(db, path):
    with open(path, 'wb') as f:
        for url in db:
            f.write(url + '\n')

html = re.sub(
    r'\b(src|background)\s*=\s*(".*?"|\'.*?\')',
    replace_url,
    sys.stdin.read(),
    flags=re.IGNORECASE,
)

print(html)

save(images, 'images.txt')
save(backgrounds, 'backgrounds.txt')
