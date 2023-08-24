#version 450 core

uniform sampler2D colorTexture;

in vec3 vert_pos;

layout(location = 0) out vec4 color;

void main() {
    vec4 pixel = texelFetch(colorTexture, ivec2(gl_FragCoord.xy), 0);
    color = pixel;
}
