#!/bin/sh

FLASK_CONFIG="copleyescalators.settings.testing.TestingConfig" python -m unittest discover
