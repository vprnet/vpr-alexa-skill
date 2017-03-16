#!/bin/bash

TARGET="http://127.0.0.1:8000/ask"

curl -v -H "Content-Type: application/json" --no-keepalive --data @$1 ${TARGET}

