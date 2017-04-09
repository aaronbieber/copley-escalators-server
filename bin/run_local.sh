#!/bin/sh

if [ -z "$VENV" ]; then
  echo "Please provide the path to your virtualenv in VENV." >&2
  exit 1
fi

echo "Using virtualenv in ${VENV}."

if [ ! -x "${VENV}/bin/uwsgi" ]; then
  echo "Couln't find uwsgi executable in ${VENV}/bin!" >&2
  echo "Install all requirements with `pip install -r requirements.txt`"
fi

FLASK_CONFIG="copleyescalators.settings.local.LocalConfig" \
            ${VENV}/bin/uwsgi \
            --http :8080 \
            -H ${VENV} \
            --py-autoreload 1 \
            --mount /=server:app
