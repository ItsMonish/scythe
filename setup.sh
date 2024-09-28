#!/bin/bash

isInstalled() {
    command -v "$1" >/dev/null 2>&1
}

if isInstalled python; then
    PYTHON_CMD=python
elif isInstalled python3; then
    PYTHON_CMD=python3
else
    echo "[!!]: Python is not installed. Please install Python."
    exit 1
fi

echo "[ii]: Python is installed: $($PYTHON_CMD --version)"

if isInstalled pip; then
    PIP_CMD=pip
elif isInstalled pip3; then
    PIP_CMD=pip3
else
    echo "[!!]: Python-pip is not installed. Please install pip."
    exit 1
fi

echo "[ii]: Python-pip is installed: $($PIP_CMD --version)"

if [ -f requirements.txt ]; then
    echo "[ii]: Installing dependencies from requirements.txt"
    $PIP_CMD install -r requirements.txt
else
    echo "[!!]: requirements.txt not found. Skipping dependency installation"
fi

echo "[ii]: Generate a Github PAT, preferably fine tuned, with write access to only the repository intended to use"
echo -n "[**]: Enter your key: "
read key

echo "GITHUB_API_KEY='$key'" > key.py

exit 0
