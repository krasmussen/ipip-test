#!/bin/bash
echo -n "Setting up virtual environment in $(pwd)/.venv... "
python3 -m venv ./.venv > /dev/null 2>&1
. ./.venv/bin/activate 
pip install -r requirements.txt > /dev/null 2>&1

echo "Done"

echo ""
echo ""

echo "To run the ipiptest.py script you will first need to source the virtual env by running:"
echo "source $(pwd)/.venv/bin/activate"
