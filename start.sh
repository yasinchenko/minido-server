#!/bin/bash
source venv/bin/activate
exec gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker
