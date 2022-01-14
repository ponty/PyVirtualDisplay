#!/bin/bash
set -e
# TODO: max-complexity=10
python3 -m flake8 . --max-complexity=11 --max-line-length=127 --extend-ignore=E203
python3 -m mypy "pyvirtualdisplay"
