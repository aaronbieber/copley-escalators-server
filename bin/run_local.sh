#!/bin/sh

FLASK_CONFIG="copleyescalators.settings.local.LocalConfig" \
  FLASK_DEBUG=1 \
  FLASK_APP=server.py flask run
