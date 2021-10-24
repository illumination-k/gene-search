#!/bin/bash

usage() {
    echo "Usage: $(basename $0) mustache-file" 1>&2
}

MUSTACHE_FILE=$1

if [ x$MUSTACHE_FILE = "x" ]; then
    echo "[ERROR]: No mustache file"
    usage
    exit 1
fi

source=$(sed -e ':loop; N; $!b loop; s/\n/ /g' $MUSTACHE_FILE | sed 's/\"/\\"/g')

TEMPLATE_FILE_NAME="${MUSTACHE_FILE%.*}.json"
TEMPLATE_FILE=$(cat << EOS
{
    "script": {
        "lang": "mustache",
        "source": "${source}"
    }
}
EOS
)

echo $TEMPLATE_FILE > $TEMPLATE_FILE_NAME