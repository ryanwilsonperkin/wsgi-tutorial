#!/bin/sh
# First run `pip3 install uwsgi`
uwsgi --http :8000 --chdir mydjangoapp --module mydjangoapp.wsgi:application
