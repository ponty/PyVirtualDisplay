#!/bin/bash
set -e
python3 -m flake8 . --max-complexity=10 --max-line-length=127 --extend-ignore=E203
python3 -m mypy "pyvirtualdisplay"
