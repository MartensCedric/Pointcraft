#version 450 core

uniform sampler2D colorTexture;

in vec3 vert_pos;
uniform float screen_width;
uniform float screen_height;

layout(location = 0) out vec4 color;

const int dither[4][4] = {
    { 0, 8, 2, 10 },
    { 12, 4, 14, 6 },
    { 3, 11, 1, 9 },
    { 15, 7, 13, 5 }
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
    int x = int(mod(xy.x, 4.0));
    int y = int(mod(xy.y, 4.0));

    float value = averaged_color;
    value *= 16.0;
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
