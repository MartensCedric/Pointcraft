# Adapted from: https://gist.github.com/bzamecnik/33e10b13aae34358c16d1b6c69e89b01
# https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
from numba import jit
import numpy as np
from PIL import Image

@jit(nopython=True)
def floyd_steinberg(image):
    # image: np.array of shape (height, width), dtype=float, 0.0-1.0
    # works in-place!
    h, w = image.shape
    for y in range(h):
        for x in range(w):
            old = image[y, x]
            new = np.round(old)
            image[y, x] = new
            error = old - new
            # precomputing the constants helps
            if x + 1 < w:
                image[y, x + 1] += error * 0.4375 # right, 7 / 16
            if (y + 1 < h) and (x + 1 < w):
                image[y + 1, x + 1] += error * 0.0625 # right, down, 1 / 16
            if y + 1 < h:
                image[y + 1, x] += error * 0.3125 # down, 5 / 16
            if (x - 1 >= 0) and (y + 1 < h): 
                image[y + 1, x - 1] += error * 0.1875 # left, down, 3 / 16
    return image

def color_gradient(w, h):
    color_gradient = []
    for row in range(h):
        interp = np.interp(row, [0, h], [0, 1])
        color_gradient.append([interp] * w)
    return np.array(color_gradient)


def pil_to_np(pilimage):
    return np.array(pilimage) / 255

def np_to_pil(image):
    return Image.fromarray((image * 255).astype('uint8'))


img_array = color_gradient(1600, 900)
out = floyd_steinberg(img_array)

image_pil = Image.fromarray(np.uint8(out * 255))
image_pil.save("output.png")

