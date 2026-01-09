#!/bin/bash
set -e

# Configuration
REPO_URL="https://github.com/prismatic-beam/paperupdater.git"
INSTALL_DIR="${HOME}/paperupdater"

# 1. Clone or Update the repository
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating paperupdater in $INSTALL_DIR..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "Cloning paperupdater to $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# 2. Install/Sync Dependencies
# --no-root skips installing the project itself as a package, which is faster for simple scripts
echo "Syncing dependencies..."
poetry install --no-root --quiet

echo "Installation complete."
echo "Please configure your .env file in $INSTALL_DIR"
echo "Then run the application using: $INSTALL_DIR/run.sh"