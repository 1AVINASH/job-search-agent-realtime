#!/bin/bash
set -e  # exit on error
set -o pipefail

echo "Starting job scraper"
docker compose up job-scraper --abort-on-container-exit

echo "Starting job parser"
docker compose up job-parser --abort-on-container-exit