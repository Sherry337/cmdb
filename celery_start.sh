#!/bin/bash
celery -A devops worker  -l info -P eventlet >> ./celery.log  &
