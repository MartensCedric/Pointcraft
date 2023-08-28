from manim import *
import numpy as np

class FloydSteinbergAlgorithm(Scene):
    def construct(self):
        image_data = np.uint8([[92, 98, 90, 85, 96, 91], [85, 82, 84, 81, 82, 86], [78, 80, 72, 75, 78, 79], [68, 72, 67, 69, 70, 68], [64, 63, 67, 62, 66, 65], [58, 59, 54, 59, 57, 60]])
        img_size = 6
        img = ImageMobject(image_data)
        img.height = img_size
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        self.play(FadeIn(img))

        # for x in range(-7, 8):
        #     for y in range(-4, 5):
        #         self.add(Dot(np.array([x, y, 0]), color=DARK_GREY))

        self.wait(1)

        # black_square = Square(fill_color=BLACK, fill_opacity=1, stroke_color=GRAY)
        # self.play(Create(black_square))

        # white_square = Square(fill_color=WHITE, fill_opacity=1, stroke_color=GRAY)
        # self.play(Create(white_square))

        text_elements = []
        for row in range(img_size):
            for col in range(img_size):
                text = Text(str(image_data[row][col]))
                x_shift = -(img_size / 2) + col
                y_shift = -(img_size / 2) + row
                text.shift((x_shift + 0.5) * RIGHT + (y_shift + 0.5) * DOWN)
                text_elements.append(text)
        text_v_group = VGroup(*text_elements)
        self.play(FadeIn(text_v_group))

