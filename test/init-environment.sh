#!/bin/bash

virtualenv -p `which python2.7` .
source bin/activate
pip install -r requirements.txt
