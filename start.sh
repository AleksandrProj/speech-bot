#!/bin/bash
if [[ $OSTYPE == "msys" ]] || [[ $OSTYPE == "win32" ]]; then
    source venv/Scripts/activate
elif [[ $OSTYPE == "darwin"* ]] || [[ $OSTYPE == "linux" ]] || [[ $OSTYPE == "linux-gnu"* ]]; then
    source venv/bin/activate
fi 
python start.py
