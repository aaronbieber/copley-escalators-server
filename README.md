# The Copley Escalators Server #

Save and retrieve the status of the often-broken escalators in the Copley Place
mall. This is a simple Flask application based heavily on the design of
https://github.com/wayfair/eggsnspam.

## Developing ##

To get started, you'll need at least Python 2.7 and `pip` installed on your
machine. This should be as simple as `brew install pip` in OS X, or use the
package manager of your choice.

This program also uses Sqlite 3 by default, so make sure you have that installed
as well. Version shouldn't be too important.

Configure a virtualenv and activate it:

```
$ virtualenv .venv
$ source .venv/bin/activate
```

Populate it with the required libraries:

```
$ pip install -r requirements.txt
```

Now run the local uwsgi server like so:

```
$ VENV=.venv bin/run_local.sh
```

## License ##

This software is provided AS IS with no restrictions or warranty of any
kind. Proceed at your peril.
