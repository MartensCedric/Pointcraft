#version 450 core

uniform sampler2D colorTexture;

in vec3 vert_pos;

layout(location = 0) out vec4 color;

void main() {
    vec4 pixel = texelFetch(colorTexture, ivec2(gl_FragCoord.xy), 0);
    float value = 0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b;
    color = vec4(value, value, value, 1.0);
}
