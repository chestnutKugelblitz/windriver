#!/usr/bin/env python3
# connexion is powerful module for REST API - it generates documentation and even UI!
"""
This is entry point of program.
"""

import connexion
from connexion.resolver import RestyResolver


def flask_init():
    """Create flask/connexion instance"""
    app = connexion.FlaskApp(__name__)
    app.add_api(
        "windriver-api.yml",
        arguments={"title": "Windriver API test"},
        resolver=RestyResolver("api"),
    )
    return app


if __name__ == "__main__":
    # development server
    flask_init().run(port=9090)
