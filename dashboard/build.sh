#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install your Python packages
pip install -r requirements.txt

# 2. Download your model and data from Hugging Face
# (Replace the links inside the quotes with your actual direct download links)
curl -L -o models/rf_model.pkl "https://huggingface.co/datasets/Prateek-1110/traffic_analyser/resolve/main/rf_model.pkl?download=true"
curl -L -o data/accidents_clean.parquet "https://huggingface.co/datasets/Prateek-1110/traffic_analyser/resolve/main/accidents_clean.parquet?download=true"

# 3. Standard Django setup commands
python manage.py collectstatic --no-input
python manage.py migrate