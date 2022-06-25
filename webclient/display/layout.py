from collections import OrderedDict

class Box:
    col_start = 0
    col_end = 0
    row_start = 0
    row_end = 0


class Layout:
    
    def __init__(self):
        self.grid = [
            [1, 2, 2, 3],
            [4, 2, 2, 5],
            [None, 6, 6, None]
        ]

        # self.grid = [
        #     [1, None, None, 3],
        #     [4, 5, 5, 6],
        #     [None, 5, 5, None]
        # ]

        self.gridMap = {1: "builtin.terminal.terminal_widget",
                        2: "builtin.gcode_renderer.gcode_render_widget",
                        3: "builtin.motion.motion_widget"}

    def generate(self) -> str:
        # build up boxes from grid tags
        boxes = OrderedDict()
        num_cols = len(self.grid[0])

        for rdx, row in enumerate(self.grid):
            print(row)
            for cdx, bid in enumerate(row):
                if not bid:  # empty spot
                    boxes[f"{cdx}-{rdx}"] = {"id": None, "cs": cdx, "ce": cdx, "rs": rdx, "re": rdx}
                else:  # box formatting
                    if bid and not bid in boxes:
                        boxes[bid] = {"id": self.gridMap.get(bid, "0"), "cs": cdx, "ce": cdx, "rs": rdx, "re": rdx}
                    else:  # box already created, update span
                        boxes[bid]["ce"] = cdx
                        boxes[bid]["re"] = rdx
        
        layout = f'<div class="grid grid-cols-{num_cols}">\n'
        boxed = list(boxes.values())

        for box in boxed:
            row_span = (box["re"] - box["rs"]) + 1
            row_span_tag = f"row-span-{row_span}" if row_span > 1 else ""

            if box["id"]:
                layout += f'<div class="col-start-{box["cs"] + 1} col-end-{box["ce"] + 2} {row_span_tag} border-2"'
                layout += f' hx-trigger="load" hx-get="/plugin/render/{box["id"]}"'
                layout += f'></div>\n'
            else:
                layout += f'<div class="col-start-{box["cs"] + 1} col-end-{box["ce"] + 2} {row_span_tag}">&nbsp;</div>'
                layout += '\n'
                
        layout += '</div>\n'
        return layout
