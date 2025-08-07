#!/bin/bash
set -e  # exit on error
set -o pipefail

cd "$(dirname "$0")"

echo "Starting job scraper"
docker compose up job-scraper --abort-on-container-exit &
docker compose up linkedin-job-scraper --abort-on-container-exit &
wait

echo "Starting job parser"
docker compose up job-parser --abort-on-container-exit