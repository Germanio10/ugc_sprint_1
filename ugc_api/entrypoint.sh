#!/bin/sh

set -e

python wait_for_kafka.py
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:8000