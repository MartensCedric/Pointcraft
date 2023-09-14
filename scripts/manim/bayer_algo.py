from manim import *
import numpy as np
from styles import *

ERR_NO = 5.4 * RIGHT
FS_R = 4.42 * RIGHT + 2.37 * UP
FS_DR = 4.42 * RIGHT + 2.42 * UP
FS_D = 3.5 * RIGHT + 2.5 * UP
FS_DL = 2 * RIGHT + 1 * UP

RES_R = 4.42 * RIGHT - 1.57 * UP
RES_DR = 4.42 * RIGHT - 2.42 * UP
RES_D = 3.5 * RIGHT - 2.5 * UP
RES_DL = 2 * RIGHT - 1 * UP

def get_image_mobject(data):
    img = ImageMobject(data)
    img.height = 8
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.set_z_index(-1)
    return img


def create_text_grid(data, size, offset, font_size):
    text_elements = []
    for row in range(size[0]):
        for col in range(size[1]):
            text = Text(str(data[row][col]), font_size=font_size)
            x_shift = -(size[0] / 2) + col + offset[0]
            y_shift = -(size[1] / 2) + row + offset[1]
            text.shift((x_shift + 0.5) * RIGHT + (y_shift + 0.5) * DOWN)
            text_elements.append(text)
    text_v_group = VGroup(*text_elements)
    return text_v_group, text_elements


def update_text_element(text_elements, coord, size, new_val):
    index = coord[1] + coord[0] * size[1]
    el = text_elements[index]
    center = el.get_center()
    color = WALTZ_WHITE
    if new_val >= 128:
        color = WALTZ_BLACK
    el.become(Text(str(new_val), font_size=el.font_size, color=color))
    el.shift(center)
    return el


def get_error_table(value):
    error_table = Table(
        [["", "*", str(int((7 / 16) * value))],
         [str(int((3 / 16) * value)), str(int((5 / 16) * value)), str(int((1 / 16) * value))]],
        include_outer_lines=True)
    return error_table


def highlight(scene, location, wait=0):
    hl_square = get_circle()
    hl_square.next_to(location)
    scene.play(Create(hl_square))
    scene.wait(wait)
    scene.play(Uncreate(hl_square))


def get_circle(radius=0.6):
    return Circle(radius=0.6, stroke_color=WALTZ_YELLOW)


class BayerAlgorithm(Scene):
    def construct(self):
        Text.set_default(font="Fira Sans")
        image_data = np.uint8(
            [[92, 98, 90, 85, 96, 91, 90, 88], [85, 82, 84, 81, 82, 86, 87, 83], [78, 80, 72, 75, 78, 79, 77, 81], [68, 72, 67, 69, 70, 68, 69, 66],
             [64, 63, 67, 62, 66, 65, 66, 67], [58, 59, 54, 59, 57, 60, 59, 58], [53, 54, 56, 52, 51, 55, 52, 53], [47, 49, 48, 47, 50, 43, 45, 47]])
        img_size = 8
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.play(FadeIn(img))

        self.wait(3)

        text_v_group, text_elements = create_text_grid(image_data, size=(8, 8), offset=(-2, 0), font_size=36)
        self.play(FadeIn(text_v_group))

        black_square = Square(fill_color=BLACK, fill_opacity=1, stroke_color=GRAY)
        black_square.shift(4 * RIGHT + 2 * UP)
        black_square_val = Text(str(0), color=WALTZ_WHITE)
        black_square_val.move_to(black_square)
        self.play(Create(black_square), Create(black_square_val))

        white_square = Square(fill_color=WHITE, fill_opacity=1, stroke_color=GRAY)
        white_square.shift(4 * RIGHT - 2 * UP)
        white_square_val = Text(str(255), color=WALTZ_BLACK)
        white_square_val.move_to(white_square)
        self.play(Create(white_square), Create(white_square_val))

        self.wait(3)
        self.play(FadeOut(black_square), FadeOut(white_square), FadeOut(white_square_val), FadeOut(black_square_val))

        # Add blue rectangles for every 2 x 2 or have 5 lines split in horizontal and v

        self.play(FadeOut(img))

