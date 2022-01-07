#!/bin/bash
exec 2>/tmp/debug.log
date >&2
set -x

if [ -z "$1" ]
  then
    echo "No file found."
    exit 1
fi

echo =====
echo $1
echo $PWD
BASEDIR=$(dirname "$0")
echo "$BASEDIR"
cd $BASEDIR
python3 upload_to_trilium.py $1
echo =====