#!/bin/sh
# First run `pip3 install uwsgi`
uwsgi --http :8000 --wsgi-file web_application.py
