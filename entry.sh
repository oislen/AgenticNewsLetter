#!/bin/sh
VENV_PYTHON="/home/ubuntu/AgenticNewsLetter/.venv/bin/python3"
exec $VENV_PYTHON -m awslambdaric "$1"