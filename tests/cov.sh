#!/bin/sh
coverage run --branch --include="*socialfeed/*" --omit="*tests*" ./manage.py test testapp
coverage html
