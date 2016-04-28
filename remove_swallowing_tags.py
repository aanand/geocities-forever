import logging
import re
import sys

log_level = logging.DEBUG if "-v" in sys.argv else logging.INFO
logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

SWALLOWING_TAG = re.compile(
    r'<!(--)?|-->|<script.*?>|<noscript.*?>|<noembed.*?>|<noframes.*?>|<style.*?>|<title.*?>|<xmp.*?>|<select.*?>|<option.*?>|http-equiv=["\']?refresh["\']?',
    flags=(re.IGNORECASE|re.DOTALL),
)

def replace(match):
    log.debug("Removing {}".format(match.group(0)))
    return ""

html = sys.stdin.read()
html = SWALLOWING_TAG.sub(replace, html)
sys.stdout.write(html)
