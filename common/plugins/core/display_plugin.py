import os

import jinja2
from flask import send_from_directory, render_template_string, Response

from .plugin import Plugin

class DisplayPlugin(Plugin):

    def __init__(self, **args):
        super().__init__(args)

        self.template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(self.plugin_path, "templates"))
        self.template_env = jinja2.Environment(loader=self.template_loader)

    def render(self) -> str:
        return "<b>N\A</b>"

    def triggered(self):
        pass

    def receive(self):
        pass

    def stream(self):
        pass

    def get_static_file(self, filename) -> Response:
        return send_from_directory(os.path.join(self.plugin_path, "static"), filename)

    # def render_template(self, template_name, **context) -> str:
    #     with open(os.path.join(self.plugin_path, "templates", template_name)) as t:
    #         template = t.read()
            
    #         return render_template_string(template, **context)

    def render_template(self, template_name, **context) -> str:
        template = self.template_env.get_template(template_name)

        return template.render(**context)