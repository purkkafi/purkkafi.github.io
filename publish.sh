#!/bin/bash

for PAGE in pages/*.bgc; do
    echo "Compiling $PAGE..."
    OUT="html/"$(basename -s .bgc "$PAGE")".html"
    beagic --module-path beagic generate_pages $PAGE $OUT
    echo "Compiled $OUT"
done
