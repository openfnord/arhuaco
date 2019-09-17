#!/bin/bash

PYTHON_COMMAND="python3"
ARHUACO_LOCATION="/usr/local/lib/python3.5/dist-packages/arhuaco/"

nohup $PYTHON_COMMAND "$ARHUACO_LOCATION"/training/train_cnn_w2v.py -t $1 </dev/null >/var/log/arhuaco/output.log 2>&1 &
