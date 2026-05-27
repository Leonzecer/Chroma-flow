import subprocess 
import sys

import gradio as gr

try:
    import webcolors

except ModuleNotFoundError:
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "webcolors"
    ])

    import webcolors


# XKCD semantic color database 호출
try:
    from matplotlib.colors import XKCD_COLORS
except ModuleNotFoundError:
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "matplotlib"
    ])

    from matplotlib.colors import XKCD_COLORS


from modules import scripts


# 초기 semantic anchor
# 현재는 기본 색 semantic만 우선 사용
# 이후 anime semantic / aesthetic semantic으로 확장 가능

BASE_COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "black": (0, 0, 0),
    "white": (255, 255, 255)
}


# HEX → RGB 변환

def hex_to_rgb(hex_color):
    return webcolors.hex_to_rgb(hex_color)


# RGB 거리 계산

def color_distance(rgb1, rgb2):
    return (
        (rgb1[0] - rgb2[0]) ** 2 +
        (rgb1[1] - rgb2[1]) ** 2 +
        (rgb1[2] - rgb2[2]) ** 2
    )


# 가장 가까운 XKCD semantic color 찾기

def find_closest_color(hex_color):

    input_rgb = hex_to_rgb(hex_color)

    closest_name = None
    closest_distance = float("inf")

    for color_name, color_hex in XKCD_COLORS.items():

        try:
            db_rgb = hex_to_rgb(color_hex)

            distance = color_distance(input_rgb, db_rgb)

            if distance < closest_distance:
                closest_distance = distance
                closest_name = color_name

        except:
            pass

    clean_name = closest_name.replace("xkcd:", "")
    clean_name = clean_name + " color"

    return clean_name


class Script(scripts.Script):

    def title(self):
        return "ChromaFlow"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):

        def generate_color_name(color):
            return find_closest_color(color)

        with gr.Row():

            with gr.Column(scale=1):

                color_picker = gr.ColorPicker(
                    label="Chroma Color",
                    interactive=True
                )

            with gr.Column(scale=2):

                color_output = gr.Textbox(
                    label="Color Identity"
                )

        color_picker.change(
            fn=generate_color_name,
            inputs=color_picker,
            outputs=color_output
        )

        return [color_picker, color_output]