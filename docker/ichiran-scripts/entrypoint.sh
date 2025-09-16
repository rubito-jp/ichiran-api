#!/bin/bash

set -euo pipefail

log() {
    printf '%s\n' "$1"
}

PGHOST="${PGHOST:-pg}"
PGUSER="${PGUSER:-postgres}"
PGPASSWORD="${PGPASSWORD:-password}"
PGDATABASE="${PGDATABASE:-postgres}"
export PGPASSWORD

log "Checking postgres server status..."
while : ; do
    if pg_isready -h "$PGHOST" -U "$PGUSER" -d "$PGDATABASE" > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

log "Postgres is ready, starting main container init."
init-all

log "Copying ichiran-cli artifacts into shared volume."
mkdir -p /ichiran-bin
cp -f /root/quicklisp/local-projects/ichiran/ichiran-cli /ichiran-bin/ichiran-cli
chmod +x /ichiran-bin/ichiran-cli
if [ -f /root/quicklisp/local-projects/ichiran/ichiran-cli.core ]; then
    cp -f /root/quicklisp/local-projects/ichiran/ichiran-cli.core /ichiran-bin/ichiran-cli.core
fi

log "All set, awaiting commands."
sleep infinity
