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
  std::vector<int32_t> grayscale_pixels;

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

    if(grayscale_pixels.size() != width * height)
      grayscale_pixels.resize(width * height);

    if (framebuffer == nullptr || framebuffer->getWidth() != width || framebuffer->getHeight() != height) {
      framebuffer = std::make_shared<Framebuffer>(width, height, false, 1);
    }

    Ref<FramebufferStack> framebufferStack = window.getFramebufferStack();
    Ref<Framebuffer> colorSource = framebufferStack->peek();
    colorSource->bind();
    colorSource->getColorAttachment(0)->bind();
    glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, pixels.data());


    //pixels_to_ppm(pixels, width, height, "buffer.ppm");
    rgba_to_grayscale(pixels, grayscale_pixels);

    for(int x = 0; x < width; x++)
    {
      for(int y = 0; y < height; y++)
      {
         int index = get_index(x, y, width);
         int32_t old_pixel = grayscale_pixels[index];
         int32_t new_pixel = 0;
         if(old_pixel >= 128)
           new_pixel = 255;
         else
           new_pixel = 0;

         grayscale_pixels[index] = new_pixel;
         int32_t error = new_pixel - old_pixel;
         if(x < width - 1)
         {
           int right_index = get_index(x+1, y, width);
           grayscale_pixels[right_index] -= static_cast<int32_t>(static_cast<float>(error) * (7.f / 16.f));
         }

         if(x < width - 1 && y < height - 1)
         {
           int bottom_right_index = get_index(x+1, y+1, width);
           grayscale_pixels[bottom_right_index] -= static_cast<int32_t>(static_cast<float>(error) * (1.f / 16.f));
         }

         if(y < height - 1)
         {
           int bottom = get_index(x, y+1, width);
           grayscale_pixels[bottom] -= static_cast<int32_t>(static_cast<float>(error) * (5.f / 16.f));
         }

         if(x > 0 && y < height - 1)
         {
           int bottom_left = get_index(x-1, y+1, width);
           grayscale_pixels[bottom_left] -= static_cast<int32_t>(static_cast<float>(error) * (3.f / 16.f));
         }
      }
    }
    grayscale_to_rgba(grayscale_pixels, pixels);

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
