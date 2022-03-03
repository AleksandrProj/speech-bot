#!/bin/bash
if [[ $OSTYPE == "msys" ]]; then
    source venv/Scripts/activate
elif [[ $OSTYPE == "darwin" ]] || [[ $OSTYPE == "linux" ]]; then
    source venv/bin/activate
fi 
python start.py
