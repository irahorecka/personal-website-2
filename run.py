"""
/run.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

A script that starts a Flask web application instance.
"""

from irahorecka import app, CONFIG

if __name__ == "__main__":
    # For development purposes only!
    try:
        app.run(host=CONFIG["local-ip"]["mac"], port=CONFIG["port"], debug=CONFIG["debug"])
    except OSError:
        app.run(host=CONFIG["local-ip"]["win"], port=CONFIG["port"], debug=CONFIG["debug"])
