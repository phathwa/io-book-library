#!/bin/sh

# Activate the virtual environment (if needed)
# source /flask-app/.venv/bin/activate

# Start the Flask app using Gunicorn on port 5000
# exec gunicorn -b 0.0.0.0:5000 main:app

# gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app
python3 setup_public_ip.py
python main.py