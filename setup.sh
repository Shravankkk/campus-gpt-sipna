#!/bin/zsh

echo "Setting up CampusGPT Sipna..."

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete."
echo "Run the app with:"
echo "source .venv/bin/activate"
echo "streamlit run app.py"
