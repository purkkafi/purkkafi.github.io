#!/bin/bash

./publish.sh

xdg-open http://0.0.0.0:8080/ &
cd html
python3 -m http.server 8080
