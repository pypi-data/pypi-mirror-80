from __future__ import annotations

from sphinx.application import Sphinx

from .handlers import html_page_context_handler
from .post_transforms import EmailAutoObfuscate
from .roles import EmailRole


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value(name="email_automode", default=True, rebuild="env")
    if app.config["email_automode"]:
        # app.add_post_transform(EmailAutoObfuscate)
        app.connect("html-page-context", html_page_context_handler)
    app.add_role("email", EmailRole())
