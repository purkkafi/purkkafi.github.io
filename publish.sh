#!/bin/bash

shopt -s globstar
set -e

beagic --module-path beagic new beagic/new_content.bgc beagic/new/new_content.html
beagic --module-path beagic rss beagic/new_content.bgc html/rss.xml

for PAGE in pages/**/*.bgc; do
    echo "Compiling $PAGE..."
    OUT="${PAGE#*/}"
    OUT="html/${OUT%.bgc}.html"
    beagic --module-path beagic generate_pages $PAGE $OUT
    echo "Compiled $OUT"
done
