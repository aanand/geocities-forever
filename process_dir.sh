#!/bin/bash

set -e

raw=$1
processed=$2

for path in $raw/*.html; do
  destination="$processed/$(basename $path)"
  cat "$path" | python ids_to_urls.py | python remove_swallowing_tags.py > "$destination"
  >&2 echo "Wrote $destination"
done
