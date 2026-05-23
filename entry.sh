#!/bin/sh
# Execute the AWS Lambda Runtime Interface Client
exec uv run python -m awslambdaric "$@"