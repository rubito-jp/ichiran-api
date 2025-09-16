#!/bin/bash

set -euo pipefail

log() {
    printf '%s\n' "$1"
}

log "Checking postgres server status..."
while : ; do
    if pg_isready -h pg > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

log "Postgres is ready, starting main container init."
init-all

log "Copying ichiran-cli into shared volume."
mkdir -p /ichiran-bin
cp -f /root/quicklisp/local-projects/ichiran/ichiran-cli /ichiran-bin/ichiran-cli
chmod +x /ichiran-bin/ichiran-cli

log "All set, awaiting commands."
sleep infinity
