#!/bin/bash

set -e

script_name="$0"
verbose=0
posargs=()

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    "-v"|"--verbose")
      verbose=1;;
    *)
      posargs+=("$1");;
  esac

  shift
done

if [[ "${#posargs[@]}" -ne 2 ]]; then
  >&2 echo "Usage: $script_name [-v|--verbose] [-p|--preserve-filenames] SOURCE_DIR TARGET_DIR"
  exit 1
fi

source_dir="${posargs[0]}"
target_dir="${posargs[1]}"

for path in $source_dir/*.html; do
  destination="${target_dir}/$(basename $path)"

  cat "$path" \
    | sed -e $'s/\x1B\[0m//' \
    | python ids_to_urls.py \
    | python remove_swallowing_tags.py \
    > "$destination"

  if [[ "$verbose" -eq 1 ]]; then
    >&2 echo "Wrote $destination"
  fi
done
