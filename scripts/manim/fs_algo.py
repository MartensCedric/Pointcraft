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


class FloydSteinbergAlgorithm(Scene):
    def construct(self):
        Text.set_default(font="Fira Sans")
        image_data = np.uint8(
            [[92, 98, 90, 85, 96, 91], [85, 82, 84, 81, 82, 86], [78, 80, 72, 75, 78, 79], [68, 72, 67, 69, 70, 68],
             [64, 63, 67, 62, 66, 65], [58, 59, 54, 59, 57, 60]])
        fs_weight = [["", "*", "7/16"], ["3/16", "5/16", "1/16"]]
        img_size = 6
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.play(FadeIn(img))

        self.wait(3)

        text_v_group, text_elements = create_text_grid(image_data, size=(6, 6), offset=(-2, 0), font_size=36)
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

        self.wait(8)
        self.play(FadeOut(black_square), FadeOut(white_square), FadeOut(white_square_val), FadeOut(black_square_val))
        first_focus_square = Square(side_length=1, color=WALTZ_YELLOW)

        first_focus_square.shift(-4.5 * RIGHT + -2.5 * DOWN)
        self.play(Create(first_focus_square))
        self.wait(8)
        self.play(FadeOut(first_focus_square))

        image_data[0,0] = 0
        update_text_element(text_elements, coord=(0, 0), size=(6, 6), new_val=0)
        print(image_data)
        img.pixel_array = image_data
        self.remove(img)
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.wait(1)
        error_text = Text(f"Error = {92} - {0} = 92")
        error_text.shift(4 * RIGHT)
        self.play(Create(error_text))
        self.wait(8)
        table = Table(
            [["", "*", "7/16"],
             ["3/16", "5/16", "1/16"]], include_outer_lines=True)
        table.shift(4 * RIGHT + 2 * UP)
        table.scale(0.5)

        fs_table_title = Text("Table for Floyd-Steinberg Dithering", font_size=24)
        fs_table_title.next_to(table, UP)

        self.play(Create(table))
        self.play(Create(fs_table_title))
        self.wait(8)
        error_table = get_error_table(92)
        error_table.shift(4 * RIGHT - 2 * UP)
        error_table.scale(0.5)
        error_table.set(width=table.width)
        self.play(Create(error_table))

        self.remove(img)
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)

        self.wait(3)
        highlight(self, RES_R, 2)
        highlight(self, FS_R, 1)
        highlight(self, ERR_NO, 1)

        highlight(self, RES_R, 0)

        arrow = Arrow(start=4 * RIGHT + 1.5 * DOWN, end=-4.36 * RIGHT + 2.55 * UP)
        self.play(GrowArrow(arrow))
        self.wait(4)
        self.play(FadeOut(arrow))

        highlight(self, RES_R, 2)

        hl_square = get_circle()
        hl_square.next_to(-4.36 * RIGHT + 2.55 * UP)
        self.play(Create(hl_square))
        self.wait(5)
        highlight(self, RES_R, 0)
        self.remove(img)
        image_data[0, 1] += 40
        update_text_element(text_elements, coord=(0, 1), size=(6, 6), new_val=image_data[0][1])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.play(Uncreate(hl_square))

        hl_rect = Rectangle(width=4.5, height=1.0, stroke_color=WALTZ_YELLOW)
        hl_rect.next_to(1.5 * RIGHT - 2.42 * UP)
        self.play(Create(hl_rect))
        self.wait(6)
        self.play(Uncreate(hl_rect))

        hl_rect = Rectangle(width=3.5, height=1.0, stroke_color=WALTZ_YELLOW)
        hl_rect.next_to(-6.6 * RIGHT + 1.5 * UP)
        self.play(Create(hl_rect))
        self.wait(5)
        self.remove(img)
        image_data[1, 1] += 5
        update_text_element(text_elements, coord=(1, 1), size=(6, 6), new_val=image_data[1][1])
        image_data[1, 0] += 28
        update_text_element(text_elements, coord=(1, 0), size=(6, 6), new_val=image_data[1][0])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.wait(3)
        self.play(Uncreate(hl_rect))



        self.remove(error_text)
        error_text = Text(f"Error = {138} - {255} = {138 - 255}", font_size=36)
        error_text.shift(4 * RIGHT)
        self.add(error_text)

        second_focus_square = Square(side_length=1, color=WALTZ_YELLOW)
        second_focus_square.next_to( -4.25 * RIGHT + -2.5 * DOWN)
        self.play(Create(second_focus_square))
        self.wait(6)
        self.remove(img)
        image_data[0, 1] = 255
        update_text_element(text_elements, coord=(0, 1), size=(6, 6), new_val=image_data[0][1])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)

        self.remove(error_table)
        error_table = get_error_table(-117)
        error_table.shift(4 * RIGHT - 2 * UP)
        error_table.scale(0.5)
        error_table.set(width=table.width)
        self.add(error_table)
        self.add(img)
        self.play(Uncreate(second_focus_square))

        self.wait(5)

        hl_rect = Rectangle(width=4.5, height=2.0, stroke_color=WALTZ_YELLOW)
        hl_rect.next_to(1.5 * RIGHT - 2 * UP)
        self.play(Create(hl_rect))
        self.wait(3)

        self.play(Uncreate(hl_rect))

        hl_rect = Rectangle(width=3.5, height=2.0, stroke_color=WALTZ_YELLOW)
        hl_rect.next_to(-5.6 * RIGHT + 2 * UP)
        self.play(Create(hl_rect))
        self.wait(3)

        self.remove(img)
        image_data[0, 2] += -51
        update_text_element(text_elements, coord=(0, 2), size=(6, 6), new_val=image_data[0][2])
        image_data[1, 2] += -7
        update_text_element(text_elements, coord=(1, 2), size=(6, 6), new_val=image_data[1][2])
        image_data[1, 1] += -36
        update_text_element(text_elements, coord=(1, 1), size=(6, 6), new_val=image_data[1][1])
        image_data[1, 0] += -21
        update_text_element(text_elements, coord=(1, 0), size=(6, 6), new_val=image_data[1][0])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.play(Uncreate(hl_rect))
        self.wait(3)

        self.play(FadeOut(error_table), FadeOut(error_text))

        for i in range(2, len(image_data) * len(image_data[0])):
            width = len(image_data[0])
            height = len(image_data)
            col = i % width
            row = int(np.floor(i / height))

            pix = image_data[row, col]
            if pix >= 128:
                pix = 255
            else:
                pix = 0
            error = image_data[row, col] - pix
            image_data[row, col] = pix
            update_text_element(text_elements, coord=(row, col), size=(6, 6), new_val=pix)

            if col + 1 < width:
                v = int(error * (7/16))
                image_data[row, col+1] += v
                update_text_element(text_elements, coord=(row, col+1), size=(6, 6), new_val=image_data[row, col+1])

            if col + 1 < width and row + 1 < height:
                v = int(error * (1/16))
                image_data[row+1, col+1] += v
                update_text_element(text_elements, coord=(row+1, col+1), size=(6, 6), new_val=image_data[row+1, col+1])

            if row + 1 < height:
                v = int(error * (5 / 16))
                image_data[row + 1, col] += v
                update_text_element(text_elements, coord=(row + 1, col), size=(6, 6),
                                    new_val=image_data[row + 1, col])

            if col - 1 >= 0 and row + 1 < height:
                v = int(error * (3 / 16))
                image_data[row + 1, col - 1] += v
                update_text_element(text_elements, coord=(row + 1, col - 1), size=(6, 6),
                                    new_val=image_data[row + 1, col - 1])

            self.remove(img)
            img = get_image_mobject(image_data)
            img.shift(-2 * RIGHT)
            self.add(img)
            self.wait(0.1)

        print(image_data)


        self.wait(6)
