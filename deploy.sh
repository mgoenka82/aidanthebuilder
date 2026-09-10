#!/usr/bin/env bash
# Deploy the current `main` to DigitalOcean App Platform, and wait for it.
#
# The app pulls from this repo's public clone URL. That source type has no
# webhook, so pushing to GitHub does not update the live site on its own -
# this script is the step that does.
set -euo pipefail

APP_ID="e6fc3b93-4883-480f-bd01-803623113468"
URL="https://aidanthebuilder-tetyi.ondigitalocean.app"

echo "==> triggering deploy of $APP_ID"
doctl apps create-deployment "$APP_ID" --format ID,Phase --no-header

echo "==> waiting for it to go live (a couple of minutes)"
while true; do
  phase=$(doctl apps list-deployments "$APP_ID" --format Phase --no-header \
          | head -1 | tr -d ' ')
  case "$phase" in
    ACTIVE)             echo "==> ACTIVE - live at $URL"; exit 0;;
    ERROR|CANCELED)     echo "==> deploy $phase"; exit 1;;
    *)                  printf '.'; sleep 10;;
  esac
done
