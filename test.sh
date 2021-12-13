#!/bin/bash

./publish.sh

xdg-open http://0.0.0.0:8080/ &
cd html
python -m http.server 8080
