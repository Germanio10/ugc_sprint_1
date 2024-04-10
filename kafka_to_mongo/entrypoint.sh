#!/bin/sh

set -e

python wait_for_kafka.py
python wait_for_mongo.py

python main.py