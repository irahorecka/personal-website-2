"""
/run.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

A script that starts a Flask web application instance.
"""

from irahorecka import app, CONFIG

if __name__ == "__main__":
    app.run(host=CONFIG["local-ip"], port=CONFIG["port"], debug=CONFIG["debug"])
