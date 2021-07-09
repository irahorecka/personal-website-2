"""
/run.py
Ira Horecka - June 2021
~~~~~~~~~~~~~~~~~~~~~~~

A script that starts a Flask web application instance.
"""

from irahorecka import app, CONFIG

if __name__ == "__main__":
    # For development purposes only!
    if CONFIG["localhost"]:
        # If you want to host purely locally with ability to use subdomain
        app.config["SERVER_NAME"] = f"localhost:{CONFIG['port']}"
        app.run(debug=CONFIG["debug"])
    else:
        # Allows access to web page via other devices on the same network
        try:
            app.run(host=CONFIG["local-ip"]["mac"], port=CONFIG["port"], debug=CONFIG["debug"])
        except OSError:
            app.run(host=CONFIG["local-ip"]["win"], port=CONFIG["port"], debug=CONFIG["debug"])
