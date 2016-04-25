import logging
import os
import re
import sys


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


in_dir = sys.argv[1]
out_dir = sys.argv[2]

SRC = re.compile(r'\bsrc\s*=\s*(".*?"|\'.*?\')')


def rewrite_embeds_file(from_path, to_path, site_name):
    with open(from_path, 'rb') as f:
        with open(to_path, 'wb') as t:
            t.write(rewrite_embeds_string(f.read(), site_name))


def rewrite_embeds_string(html, site_name):
    def replace(match):
        group = match.group(1)
        quote_char = group[0]
        src = group[1:-1]

        if src.startswith('http'):
            return group

        src = os.path.join('/', site_name, src)
        if not src.startswith('/'):
            src = '/' + src
        src = "http://www.oocities.org{}".format(src)

        replacement = "src={}{}{}".format(quote_char, src, quote_char)

        log.debug(" -> Rewriting {} to {}".format(match.group(0), replacement))
        return replacement

    return SRC.sub(replace, html)


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
