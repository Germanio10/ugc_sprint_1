#!/bin/bash

sleep 15

python3 utils/wait_for_kafka.py

pytest
