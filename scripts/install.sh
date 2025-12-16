#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip

python3 -m venv .venv

. .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Installed. Activate venv: source .venv/bin/activate"
