#version 450 core

uniform sampler2D colorTexture;

in vec3 vert_pos;
uniform float screen_width;
uniform float screen_height;

layout(location = 0) out vec4 color;

int dither[8][8] = {
    { 24, 10, 12, 26, 35, 47, 49, 37 },
    { 8, 0, 2, 14, 45, 59, 61, 51 },
    { 22, 6, 4, 16, 43, 57, 63, 53 },
    { 30, 20, 18, 28, 33, 41, 55, 39 },
    { 34, 46, 48, 36, 25, 11, 13, 27 },
    { 44, 58, 60, 50, 9, 1, 3, 15 },
    { 42, 56, 62, 52, 23, 7, 5, 17 },
    { 32, 40, 54, 38, 31, 21, 19, 29 }
};

float rgb_to_grayscale(vec3 rgb_val)
{
    return 0.299 * rgb_val.r + 0.587 * rgb_val.g + 0.114 * rgb_val.b;
}

void main() {
    vec2 screen = vec2(screen_width, screen_height);
    float down_sample = 5.0;
    vec2 desired_res = screen / down_sample;
    vec2 normalized_coord = floor((gl_FragCoord.xy / screen) * desired_res) / desired_res;
    vec2 centered_coord = normalized_coord + vec2(0.5, 0.5) / desired_res;

    vec2 texel_size = 1.0 / screen;

    int kernel_size = 2;
    float sum_color = 0.0;
    for (int x = -kernel_size; x <= kernel_size; ++x) {
        for (int y = -kernel_size; y <= kernel_size; ++y) {
            vec2 offset = vec2(float(x), float(y)) * texel_size;
            vec2 offset_coord = centered_coord + offset;
            sum_color += rgb_to_grayscale(texture(colorTexture, offset_coord).rgb);
        }
    }

    int samples = (2 * kernel_size + 1) * (2 * kernel_size + 1);
    float averaged_color = sum_color / float(samples);

    vec2 xy = ivec2(normalized_coord * desired_res);
    int x = int(mod(xy.x, 8.0));
    int y = int(mod(xy.y, 8.0));

    float value = averaged_color;
    value *= 64.0;
    value = round(value);
    if (float(dither[x][y]) < value)
    {
        value = 1.0;
    }
    else
    {
        value = 0.0;
    }

    color = vec4(value, value, value, 1.0);
}
