#!/bin/sh

set -e

python wait_for_kafka.py

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:8000