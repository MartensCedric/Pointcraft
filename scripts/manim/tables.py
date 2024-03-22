from manim import *
import numpy as np
from styles import *


class TablesScene(Scene):
    def construct(self):
        Text.set_default(font="Fira Sans")
        bayer2_2_table = Table([["0", "127"], ["191", "63"]], include_outer_lines=True)
        self.play(FadeIn(bayer2_2_table))
        self.wait(1)
        self.play(Circumscribe(bayer2_2_table))
        self.wait(2)
        self.play(FadeOut(bayer2_2_table))
        bayer4_4_table = Table([["0", "8", "2", "10"], ["12", "4", "14", "6"], ["3", "11", "1", "9"], ["15", "7", "13", "5"]], include_outer_lines=True)
        self.play(FadeIn(bayer4_4_table))
        self.wait(1)
        self.play(Circumscribe(bayer4_4_table))
        self.wait(2)
        self.play(FadeOut(bayer4_4_table))

        bayer8_8_table = Table([["0", "32", "8", "40", "2", "34", "10", "42"], ["48", "16", "56", "24", "50", "18", "58", "26"], ["12", "44", "4", "36", "14", "46", "6", "38"], ["60", "28", "52", "20", "62", "30", "54", "22"], ["3", "35", "11", "43", "1", "33", "9", "41"], ["51", "19", "59", "27", "49", "17", "57", "25"], ["15", "47", "7", "39", "13", "45", "5", "37"], ["63", "31", "55", "23", "61", "29", "53", "21"]], include_outer_lines=True)
        bayer8_8_table.scale(0.5)
        self.play(FadeIn(bayer8_8_table))
        self.wait(1)
        self.play(Circumscribe(bayer8_8_table))
        self.wait(2)
        self.play(FadeOut(bayer8_8_table))

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": True}):
        scene = TablesScene()
        scene.render()
