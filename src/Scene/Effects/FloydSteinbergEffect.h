//
// Created by cedric on 8/23/23.
//

#ifndef POINT_CRAFT_FLOYDSTEINBERGEFFECT_H
#define POINT_CRAFT_FLOYDSTEINBERGEFFECT_H

#include "../../Rendering/ColorRenderPass.h"
#include "PostProcessEffect.h"
#include "../../Rendering/RenderingUtil.h"

class FloydSteinbergEffect : public PostProcessEffect {

  std::vector<uint8_t> pixels;
  std::vector<uint32_t> grayscale_pixels;

public:
  FloydSteinbergEffect(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/floyd_steinberg"),
                          enabled) {
  }

  void renderGui() override {
    ImGui::Checkbox("Enable Floyd-Steinberg effect", &enabled);

//    if (enabled) {
//      ImGui::SliderFloat("Aberration start", &aberrationStart, 0.5, 3);
//      ImGui::SliderFloat("Aberration R Offset", &aberrationROffset, -0.01, 0.01);
//      ImGui::SliderFloat("Aberration G Offset", &aberrationGOffset, -0.01, 0.01);
//      ImGui::SliderFloat("Aberration B Offset", &aberrationBOffset, -0.01, 0.01);
//    }
  }
  void render() override {
    if (!enabled) {
      return;
    }

    Window& window = Window::instance();
    int32_t width = window.getWindowWidth();
    int32_t height = window.getWindowHeight();

    if(pixels.size() != width * height * 4)
      pixels.resize(width * height * 4);

//    if(grayscale_pixels.size() != width * height)
//      grayscale_pixels.resize(width * height);

    if (framebuffer == nullptr || framebuffer->getWidth() != width || framebuffer->getHeight() != height) {
      framebuffer = std::make_shared<Framebuffer>(width, height, false, 1);
    }

    Ref<FramebufferStack> framebufferStack = window.getFramebufferStack();
    Ref<Framebuffer> colorSource = framebufferStack->peek();    colorSource->getColorAttachment(0)->bind();
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels.data());
    colorSource->getColorAttachment(0)->unbind();
    colorSource->bind();
    glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, pixels.data());

    //pixels_to_ppm(pixels, width, height, "buffer.ppm");
//    rgba_to_grayscale(pixels, grayscale_pixels);
//
//    for(int i = 0; i < width * height; i++)
//    {
//      pixels[i*4] = grayscale_pixels[i];
//      pixels[i*4+1] = grayscale_pixels[i];
//      pixels[i*4+2] = grayscale_pixels[i];
//      pixels[i*4+3] = 255;
//    }

    colorSource->getColorAttachment(0)->bind();
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels.data());
    colorSource->getColorAttachment(0)->unbind();

    framebufferStack->push(framebuffer, 1);

    update();
    ColorRenderPass::renderTextureWithEffect(colorSource->getColorAttachment(0), shader);

    Ref<Framebuffer> resultFbo = framebufferStack->pop();
    ColorRenderPass::renderTexture(resultFbo->getColorAttachment(0));
  }
  void update() override {
//    shader->setFloat("start", aberrationStart);
//    shader->setFloat("rOffset", aberrationROffset);
//    shader->setFloat("gOffset", aberrationGOffset);
//    shader->setFloat("bOffset", aberrationBOffset);
  }
};

#endif  //POINT_CRAFT_FLOYDSTEINBERGEFFECT_H
