#!/usr/bin/env sh
set -e
echo "Building..."
docker ps > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Docker is not running, please start docker and try again."
  exit 1
fi
docker compose build --no-cache