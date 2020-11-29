#!/usr/bin/env bash

set -e
set -x

pytest --cov=app --cov-config=.coveragerc --cov-report=term-missing app/tests "${@}"