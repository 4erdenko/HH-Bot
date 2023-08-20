#!/bin/bash

printenv | sed 's/^\(.*\)$/export \1/g' > /app/env.sh

chmod +x /app/main.py

{
  echo '@reboot . /app/env.sh; python3 /app/main.py >> /app/cron.log 2>&1'
  echo '0 */4 * * * . /app/env.sh; python3 /app/main.py >> /app/cron.log 2>&1'
} | crontab -

cron -f &

tail -f /app/cron.log &
wait
