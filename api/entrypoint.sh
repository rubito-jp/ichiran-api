#!/bin/sh
set -eu

while [ ! -x /ichiran-bin/ichiran-cli ]; do
    echo 'Waiting for ichiran-cli...'
    sleep 2
done

while [ ! -f /ichiran-bin/jmdictdb/jmdictdb/data/conj.csv ]; do
    echo 'Waiting for jmdictdb data...'
    sleep 2
done

mkdir -p /root
if [ -e /root/jmdictdb ] || [ -L /root/jmdictdb ]; then
    rm -rf /root/jmdictdb
fi
ln -s /ichiran-bin/jmdictdb /root/jmdictdb

exec uvicorn main:app --host 0.0.0.0 --port 8000
