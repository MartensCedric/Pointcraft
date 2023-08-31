#version 450 core

uniform sampler2D colorTexture;

in vec3 vert_pos;
uniform float screen_width;
uniform float screen_height;

layout(location = 0) out vec4 color;

int dither[2][2] = {{0, 2}, {3, 1}};

void main() {
    vec4 pixel = texelFetch(colorTexture, ivec2(gl_FragCoord.xy), 0);
    vec2 xy = ivec2(gl_FragCoord.x * screen_width, gl_FragCoord.y * screen_height);
    int x = int(mod(xy.x, 2.0));
    int y = int(mod(xy.y, 2.0));
    float value = 0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b;

    value *= 4.0;
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
