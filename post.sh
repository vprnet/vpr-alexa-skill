#!/bin/bash

TARGET="https://vpr-sisu.herokuapp.com/ask"
CURL_ARGS='-v -H "Content-Type: application/json" --no-keepalive'

curl ${CURL_ARGS} --data-binary @$1 ${TARGET}
