import logging
import os
import random
import re
import sys


all_paths = []
log_level = logging.INFO
output_dir = "site/html"

posargs = iter(sys.argv[1:])

while True:
    try:
        arg = next(posargs)
    except StopIteration:
        break

    if arg in ("-v", "--verbose"):
        log_level = logging.DEBUG
    elif arg == "--output-dir":
        output_dir = next(posargs)
    elif arg.startswith("-"):
        raise SystemExit("Unrecognised option: {}".format(arg))
    else:
        all_paths.append(arg)


logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

LINK = re.compile(
    r'\bhref=(".*?"|\'.*?\')',
    flags=(re.IGNORECASE|re.DOTALL),
)

all_names = [os.path.basename(path) for path in all_paths]

def rewrite_link(match):
    group = match.group(1)
    quote_char = group[0]
    new_href = random.choice(all_names)
    replacement = "href={}{}{}".format(quote_char, new_href, quote_char)
    logging.debug("  {}".format(replacement))
    return replacement

for raw_path in all_paths:
    processed_path = os.path.join(output_dir, os.path.basename(raw_path))
    logging.debug("{} -> {}".format(raw_path, processed_path))

    with open(raw_path, 'rb') as f:
        html = f.read()

    html = LINK.sub(rewrite_link, html)

    with open(processed_path, 'wb') as f:
        f.write(html)
