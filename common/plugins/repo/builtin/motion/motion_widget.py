from flask import render_template, request, jsonify, current_app, Response

from common.plugins.core import DisplayPlugin


class MotionWidget(DisplayPlugin):
    def __init__(self):
        description = "The standard control widget to drive the connected machine"
        super().__init__(description=description)

    def render(self) -> str:
        return f"""
    <button type="button" hx-vals='{{"dir":"left", "len":5}}' hx-swap="none" hx-post="/plugins/post/{self.id}">Press</button>
    """

    def receive(self) -> Response:
        vars = (dict(request.form))
        
        if vars["dir"] == "left":
            print("GO LEFT")
        else:
            print("GO ELSEWHERE")
        # # did we get valid data?
        # payload = {}
        # if request.is_json:
        #     payload = request.get_json()
        #     print("payload ", payload)
        # else:
        #     return jsonify({"error": "request was not proper"})

        return jsonify({"action": "ok!"})