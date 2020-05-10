#!/bin/sh
set -e
autoflake  -i -r --remove-all-unused-imports .
autoflake  -i -r --remove-unused-variables .
isort --recursive .
black .
