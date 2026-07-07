#!/bin/bash

cd "$(dirname "$0")"

python3 entrainement.py >> reentrainement.log 2>&1
echo "Reentrainement du $(date)" >> reentrainement.log
