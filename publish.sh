#!/bin/bash

shopt -s globstar

for PAGE in pages/**/*.bgc; do
    echo "Compiling $PAGE..."
    OUT="${PAGE#*/}"
    OUT="html/${OUT%.bgc}.html"
    beagic --module-path beagic generate_pages $PAGE $OUT
    echo "Compiled $OUT"
done
