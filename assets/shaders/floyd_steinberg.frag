#version 450 core

uniform sampler2D colorTexture;
uniform float u_hue;

in vec3 vert_pos;

layout(location = 0) out vec4 color;
vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
    vec4 pixel = texelFetch(colorTexture, ivec2(gl_FragCoord.xy), 0);
    //vec3 color2 = hsv2rgb(vec3(mod(u_hue / 255.0 + gl_FragCoord.x / 1280 + gl_FragCoord.y / 720, 1.0), 1.0, 1.0));

    if(pixel.r + pixel.g + pixel.b <= 0.01) {

        color = vec4(0.0);
        return;
    }

    vec3 hsv = rgb2hsv(pixel.rgb);
    hsv.b = 1.0;
    color = vec4(hsv2rgb(hsv), pixel.a);
}
