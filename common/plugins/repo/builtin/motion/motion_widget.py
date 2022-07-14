import json
import time

from flask import render_template, request, jsonify, current_app, Response

from common.plugins.core import DisplayPlugin

class MotionMonitor:
    current_axis_movement = None  # type: str
    current_press_start = 0
    is_locked = False

    def __enter__(self):
        print("connected motion")
        return self
  
    def __exit__(self, exc_type, exc_value, traceback):
        print("Disconnected motion")

class MotionWidget(DisplayPlugin):
    def __init__(self):
        description = "The standard control widget to drive the connected machine"
        super().__init__(description=description)

    def render(self) -> str:
        return self.render_template("controls.html", id=self.id)
    #     return f"""
    # <button type="button" hx-vals='{{"dir":"left", "len":5}}' hx-swap="none" hx-post="/plugins/post/{self.id}">Press</button>
    # """

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

    def stream(self, websocket) -> str:
        print("connected motion socket")
        with MotionMonitor() as m:
            press_start = 0
            n = 0
            while True:
                sent = websocket.receive(timeout=0.2)
                n += 1
                if sent:
                    html = ""
                    data = json.loads(sent)
                    headers = data.pop("HEADERS")
                    print(data)
                    if "axis-button-movement" in data:  # axis movement
                        command = data["axis-button-movement"]
                        state = data["axis-button-state"]

                        print(command, " ", state)
                        if not command in ["Xmin", "Xplus", "Ymin", "Yplus", "Zmin", "Zplus", "Amin", "Aplus"]:
                            print("Unrecognized axis direction")
                            return

                        result = self.handle_input(command, state, time.time() - m.current_press_start)

                        if state == "down" and not m.current_axis_movement:  # new press
                            m.current_axis_movement = command
                            m.current_press_start = time.time()
                            print("starting press in ", command)
                        elif state == "down":  # continued press
                            print("still pressing in ", m.current_axis_movement)

                        next_button_state = "up"
                        if state == "up":
                            m.current_axis_movement = None  # finished press
                            next_button_state = "down"
                            duration = time.time() - m.current_press_start
                            print("press duration ", duration)

                        button_symbol = {"Xmin": "&larr;", "Xplus": "&rarr;", "Ymin": "&darr;", "Yplus": "&uarr;",
                                         "Zmin": "&darr;", "Zplus": "&uarr;"}
                        key_bindings = {"Xmin": 37, "Xplus": 39, "Ymin": 40, "Yplus": 38,
                                         "Zmin": "&darr;", "Zplus": "&uarr;"}
                        html = self.render_template("direction_button.html",
                                                            button_movement=command,
                                                            mouse_event=next_button_state,
                                                            state_value=next_button_state,
                                                            movement_value=command,
                                                            button_content=button_symbol[command],
                                                            key_binding=f"keyCode=={key_bindings[command]}")
                        # print(html)
                        websocket.send(html)

    def handle_input(self, command, state, duration) -> str:
        if state == "down":
            current_app.request_conn.send_string("KEYPRESS")
            results = current_app.request_conn.recv_string()
            print(results)

        return "blaat"
