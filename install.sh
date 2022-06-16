#!/bin/bash
python -m venv venv
if [[ $OSTYPE == "msys" ]]; then
    source venv/Scripts/activate
elif [[ $OSTYPE == "darwin" ]] || [[ $OSTYPE == "linux" ]]; then
    source venv/bin/activate
fi
pip install -r requirements.txt
