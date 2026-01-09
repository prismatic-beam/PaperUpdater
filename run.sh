#!/bin/bash
set -e

# Navigate to the script directory to ensure correct execution context
cd "$(dirname "$0")"

# Run the Updater
# 'poetry run' executes the command inside the virtual environment
# "$@" passes any arguments (like --restore or --verbose) from this bash script to python
echo "Executing PaperUpdater..."
poetry run python src/main.py "$@"