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


def highlight(scene, location, wait=0, c=WALTZ_YELLOW):
    hl_square = get_circle(radius=0.6, c=c)
    hl_square.next_to(location)
    scene.play(Create(hl_square))
    scene.wait(wait)
    scene.play(Uncreate(hl_square))


def get_circle(radius=0.6, c=WALTZ_YELLOW):
    return Circle(radius=0.6, stroke_color=c)


def create_lines(n):
    lines = []
    for i in range(n):
        l = Line(start=[-6 + i * 2, 4, 0], end=[-6 + i * 2,  -4, 0], color=WALTZ_BLUE)
        lines.append(l)
    for i in range(n):
        l = Line(start=[-6, 4 - i * 2, 0], end=[2, 4 - i * 2, 0], color=WALTZ_BLUE)
        lines.append(l)
    return lines

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
        bayer2_2_table = Table([["0", "127"], ["191", "63"]], include_outer_lines=True)
        bayer2_2_table.scale(0.75)
        bayer2_2_table.shift(4.5 * RIGHT + 2 * UP)
        self.play(Create(bayer2_2_table))

        lines = create_lines(5)
        for l in lines:
            self.play(Create(l, run_time=0.4))

        focus_square = Square(side_length=2, color=WALTZ_YELLOW)
        focus_square.next_to(-6.25 * RIGHT + 3 * UP)
        self.play(Create(focus_square))

        self.play(Wiggle(bayer2_2_table))

        first_comp = Text("92 > 0", color=WALTZ_WHITE)
        first_comp.shift(4.5 * RIGHT - UP)
        self.play(FadeIn(first_comp))
        self.wait(2)
        highlight(self, bayer2_2_table.get_center() + 0.5* UP + 1.70* LEFT, wait=1, c=WALTZ_GREEN)
        highlight(self, focus_square.get_center() + 0.5* UP + 1.35* LEFT, wait=1, c=WALTZ_GREEN)
        self.wait(2)
        self.remove(img)
        image_data[0,0] = 255
        update_text_element(text_elements, coord=(0, 0), size=(8, 8), new_val=image_data[0][0])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)

        self.wait(2)
        second_comp = Text("98 ≯ 127", color=WALTZ_WHITE)
        second_comp.next_to(first_comp, DOWN)
        self.play(FadeIn(second_comp))
        self.wait(2)
        self.remove(img)
        image_data[0,1] = 0
        update_text_element(text_elements, coord=(0, 1), size=(8, 8), new_val=image_data[0][1])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.wait(2)

        third_comp = Text("85 ≯ 191", color=WALTZ_WHITE)
        third_comp.next_to(second_comp, DOWN)
        self.play(FadeIn(third_comp))
        self.wait(2)
        self.remove(img)
        image_data[1,0] = 0
        update_text_element(text_elements, coord=(1, 0), size=(8, 8), new_val=image_data[1][0])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.wait(2)


        fourth_comp = Text("82 > 63", color=WALTZ_WHITE)
        fourth_comp.next_to(third_comp, DOWN)
        self.play(FadeIn(fourth_comp))
        self.remove(img)
        image_data[1,1] = 255
        update_text_element(text_elements, coord=(1, 1), size=(8, 8), new_val=image_data[1][1])
        img = get_image_mobject(image_data)
        img.shift(-2 * RIGHT)
        self.add(img)
        self.wait(2)

        self.play(Uncreate(focus_square))
        self.play(FadeOut(first_comp, second_comp, third_comp, fourth_comp))

        arrow = Arrow(np.array([-1, 3, 0]), np.array([-1, -3, 0]), buff=0, stroke_width=60)
        arrow.scale(1)
        arrow.set_color(WALTZ_RED)

        self.play(Create(arrow))
        self.wait(2)
        self.play(Uncreate(arrow))

        for i in range(1, 16):
            self.remove(img)
            block_row = i // 4
            block_col = i % 4
            r = block_row * 2
            c = block_col * 2
            image_data[r, c] = 255 if image_data[r, c] > 0 else 0
            image_data[r+1, c] = 255 if image_data[r+1, c] > 127 else 0
            image_data[r, c+1] = 255 if image_data[r, c+1] > 191 else 0
            image_data[r+1, c+1] = 255 if image_data[r+1, c+1] > 63 else 0
            img = get_image_mobject(image_data)
            img.shift(-2 * RIGHT)
            self.add(img)
            update_text_element(text_elements, coord=(r, c), size=(8, 8), new_val=image_data[r, c])
            update_text_element(text_elements, coord=(r+1, c), size=(8, 8), new_val=image_data[r+1,c])
            update_text_element(text_elements, coord=(r, c+1), size=(8, 8), new_val=image_data[r,c+1])
            update_text_element(text_elements, coord=(r+1, c+1), size=(8, 8), new_val=image_data[r+1, c+1])
            self.wait(3 / i)

        self.wait(5)


if __name__ == '__main__':
    with tempconfig({"quality": "medium_quality", "disable_caching": True}):
        scene = BayerAlgorithm()
        scene.render()