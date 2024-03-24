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
        data_4 = [["0", "8", "2", "10"], ["12", "4", "14", "6"], ["3", "11", "1", "9"], ["15", "7", "13", "5"]]
        data_4_good = []
        for array in data_4:
            arr = []
            for a in array:
                arr.append(str(int(a) * 16))
            data_4_good.append(arr)
        bayer4_4_table = Table(data_4_good, include_outer_lines=True)
        self.play(FadeIn(bayer4_4_table))
        self.wait(1)
        self.play(Circumscribe(bayer4_4_table))
        self.wait(2)
        self.play(FadeOut(bayer4_4_table))
        data_8 = [["0", "32", "8", "40", "2", "34", "10", "42"], ["48", "16", "56", "24", "50", "18", "58", "26"], ["12", "44", "4", "36", "14", "46", "6", "38"], ["60", "28", "52", "20", "62", "30", "54", "22"], ["3", "35", "11", "43", "1", "33", "9", "41"], ["51", "19", "59", "27", "49", "17", "57", "25"], ["15", "47", "7", "39", "13", "45", "5", "37"], ["63", "31", "55", "23", "61", "29", "53", "21"]]
        data_8_good = []
        for array in data_8:
            arr = []
            for a in array:
                arr.append(str(int(a) * 4))
            data_8_good.append(arr)
        bayer8_8_table = Table(data_8_good, include_outer_lines=True)
        bayer8_8_table.scale(0.5)
        self.play(FadeIn(bayer8_8_table))
        self.wait(1)
        self.play(Circumscribe(bayer8_8_table))
        self.wait(2)
        self.play(FadeOut(bayer8_8_table))
        self.wait(2)
        bayer2_2_percent_table = Table([["0 (0%)", "127 (50%)"], ["191 (75%)", "63 (25%)"]], include_outer_lines=True)
        self.play(FadeIn(bayer2_2_percent_table))
        self.wait(1)
        self.play(Circumscribe(bayer2_2_percent_table))
        self.wait(2)
        self.play(FadeOut(bayer2_2_percent_table))

if __name__ == '__main__':
    with tempconfig({"quality": "high_quality", "disable_caching": True}):
        scene = TablesScene()
        scene.render()
