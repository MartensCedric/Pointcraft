# Adapted from: https://gist.github.com/bzamecnik/33e10b13aae34358c16d1b6c69e89b01
# https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
import numpy as np
from PIL import Image
import sys

def floyd_steinberg(image, weight=1):
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
                image[y, x + 1] += error * 0.4375 * weight # right, 7 / 16
            if (y + 1 < h) and (x + 1 < w):
                image[y + 1, x + 1] += error * 0.0625 * weight# right, down, 1 / 16
            if y + 1 < h:
                image[y + 1, x] += error * 0.3125 * weight# down, 5 / 16
            if (x - 1 >= 0) and (y + 1 < h):
                image[y + 1, x - 1] += error * 0.1875 * weight# left, down, 3 / 16
    return image
bayer_matrix = np.array([
    [0, 2],
    [3, 1]
])

def bayer(image):
    h, w = image.shape
    bayer_tiled = np.tile(bayer_matrix, (h // 2, w // 2))  # Tile the Bayer matrix

    print(bayer_tiled)
    for y in range(h):
        for x in range(w):
            old = image[y, x]
            new = 1 if bayer_tiled[y, x] < np.round(old * 4.0) else 0
            image[y, x] = new
    return image


def color_gradient(w, h):
    color_gradient = []
    for row in range(h):
        x = list(range(w))
        interp = np.interp(x, [0, w-1], [0, 1])
        color_gradient.append(interp)
    return np.array(color_gradient)

def bad_color_gradient(w, h):
    color_gradient = []
    for row in range(h):
        x = list(range(w))
        interp = np.interp(x, [0, w-1], [0.2, 0.8])
        color_gradient.append(interp)
    return np.array(color_gradient)

def gamma_correction(arr, gamma):
    return arr**(1/gamma)

def pil_to_np(pilimage):
    return np.array(pilimage) / 255

def np_to_pil(image):
    return Image.fromarray((image * 255).astype('uint8'))

good_gradient = color_gradient(225, 50)
Image.fromarray(np.uint8(good_gradient * 255)).save("good_gradient.png")

bad_gradient = bad_color_gradient(225, 50)
Image.fromarray(np.uint8(bad_gradient * 255)).save("bad_gradient.png")

gamma_corrected = gamma_correction(good_gradient.copy(), 0.594)
Image.fromarray(np.uint8(gamma_corrected * 255)).save("gamma_correction.png")

fs_bad_gradient = floyd_steinberg(bad_gradient)
Image.fromarray(np.uint8(fs_bad_gradient * 255)).save("fs_bad_gradient.png")
fs_good_gradient = floyd_steinberg(good_gradient.copy())
Image.fromarray(np.uint8(fs_good_gradient * 255)).save("fs_good_gradient.png")

fs_gamma_corrected = floyd_steinberg(gamma_corrected.copy())
Image.fromarray(np.uint8(fs_gamma_corrected * 255)).save("good_gamma.png")

fs_gamma_corrected_and_weighted = floyd_steinberg(gamma_corrected.copy(), 0.741)
Image.fromarray(np.uint8(fs_gamma_corrected_and_weighted * 255)).save("good_gamma_weighted.png")

normal_gradient = color_gradient(256, 48)
bayer_done = bayer(normal_gradient)
np_to_pil(bayer_done).save('bayer_gradient.png')

if len(sys.argv) > 1:
    filename  = sys.argv[1]
    img = Image.open(filename).convert("L")
    img = img.resize((240, 135), Image.NEAREST)
    img = pil_to_np(img.copy())
    img = gamma_correction(img.copy(), 0.594)
    img = floyd_steinberg(img.copy(), 0.7)
    # img = img.resize((1920, 1080), Image.NEAREST)
    img = np_to_pil(img.copy())
    img.save("output.png")


