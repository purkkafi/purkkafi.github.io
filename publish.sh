#!/bin/bash

shopt -s globstar
set -e

beagic --module-path beagic rss beagic/new_local.bgc html/rss.xml
./aggregate_rss.py
beagic --module-path beagic new beagic/new_content.bgc beagic/new/new_content.html
beagic --module-path beagic lenkkipuu beagic/new_content.bgc html/lenkkipuu/index.html

for PAGE in pages/**/*.bgc; do
    echo "Compiling $PAGE..."
    OUT="${PAGE#*/}"
    OUT="html/${OUT%.bgc}.html"
    beagic --module-path beagic generate_pages $PAGE $OUT
    echo "Compiled $OUT"
done
