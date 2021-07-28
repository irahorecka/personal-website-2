"""
/run.py
Ira Horecka - July 2021
~~~~~~~~~~~~~~~~~~~~~~~

Starts a Flask web application instance.
"""

from irahorecka import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
