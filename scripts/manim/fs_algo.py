from manim import *
import numpy as np
from styles import *

def get_image_mobject(data):
    img = ImageMobject(data)
    img.height = 6
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
    index = coord[1] +  coord[0] * size[1]
    el = text_elements[index]
    center = el.get_center()
    el.become(Text(str(new_val), font_size=el.font_size))
    el.shift(center)
    return el

def get_error_table(value):
    error_table = Table(
        [["", "*", str(int((7/16)*value))],
        [str(int((3/16)*value)),str(int((5/16)*value)), str(int((1/16)*value))]],
    include_outer_lines=True)
    return error_table

class FloydSteinbergAlgorithm(Scene):
    def construct(self):
        Text.set_default(font="Fira Sans")
        image_data = np.uint8([[92, 98, 90, 85, 96, 91], [85, 82, 84, 81, 82, 86], [78, 80, 72, 75, 78, 79], [68, 72, 67, 69, 70, 68], [64, 63, 67, 62, 66, 65], [58, 59, 54, 59, 57, 60]])
        fs_weight = [["", "*", "7/16"], ["3/16", "5/16", "1/16"]]
        img_size = 6
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.play(FadeIn(img))

        self.wait(1)

        # black_square = Square(fill_color=BLACK, fill_opacity=1, stroke_color=GRAY)
        # self.play(Create(black_square))

        # white_square = Square(fill_color=WHITE, fill_opacity=1, stroke_color=GRAY)
        # self.play(Create(white_square))
        text_v_group, text_elements = create_text_grid(image_data, size=(6,6), offset=(-2,0), font_size=36)
        self.play(FadeIn(text_v_group))
        first_focus_square = Square(side_length=1, color=WALTZ_YELLOW)

        # first_focus_square.shift(-2.5 * RIGHT + -2.5 * DOWN)
        # self.play(Create(first_focus_square))

        image_data[0][0] = 0
        update_text_element(text_elements, coord=(0,0), size=(6,6), new_val=0)
        # print(image_data)
        # img.pixel_array = image_data
        self.remove(img)
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.wait(1)
        table = Table(
            [["", "*", "7/16"],
            ["3/16","5/16", "1/16"]], include_outer_lines=True)
        table.shift(4 * RIGHT + 2 * UP)
        table.scale(0.5)

        self.play(Create(table))
        error_text = Text(f"Error = {92} - {0} = 92")
        error_text.shift(4* RIGHT)
        self.play(Create(error_text))
        error_table = get_error_table(92)
        error_table.shift(4 * RIGHT - 2 * UP)
        error_table.scale(0.5)
        self.play(Create(error_table))
        # fs_weights_v_group, _ = create_text_grid(fs_weight, size=(2,3), offset=(3, -2), font_size=24)
        # self.play(FadeIn(fs_weights_v_group))
        self.wait(2)

