#!/bin/bash

TARGET="https://vpr-sisu.herokuapp.com/ask"

curl -v -H "Content-Type: application/json" --no-keepalive --data @$1 ${TARGET}
