from copleyescalators import app

# Provides the "callable" WSGI server that uWSGI wants.
# Mount this as `--mount /=server:app`
app = app.create_app()
