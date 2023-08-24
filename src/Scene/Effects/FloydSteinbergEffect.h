//
// Created by cedric on 8/23/23.
//

#ifndef POINT_CRAFT_FLOYDSTEINBERGEFFECT_H
#define POINT_CRAFT_FLOYDSTEINBERGEFFECT_H

#include "../../Rendering/ColorRenderPass.h"
#include "PostProcessEffect.h"

class FloydSteinbergEffect : public PostProcessEffect {

  std::vector<uint8_t> pixels;
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

    if (framebuffer == nullptr || framebuffer->getWidth() != width || framebuffer->getHeight() != height) {
      framebuffer = std::make_shared<Framebuffer>(width, height, false, 1);
    }

    Ref<FramebufferStack> framebufferStack = window.getFramebufferStack();
    Ref<Framebuffer> colorSource = framebufferStack->peek();
    colorSource->bind();
    glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE, pixels.data());

    std::ofstream ppm_file("buffer.ppm", std::ios::binary);
    if (!ppm_file.is_open()) {
      std::cerr << "Error opening file: " << "buffer.ppm" << std::endl;
      return;
    }

    ppm_file << "P3\n" << width << " " << height << "\n255\n";

    for(int i = 0; i < width*height; i++)
    {
      uint8_t red = pixels[i * 4];
      uint8_t green = pixels[i * 4 + 1];
      uint8_t blue = pixels[i * 4 + 2];

      ppm_file << std::to_string(red) << ' ';
      ppm_file << std::to_string(green) << ' ';
      ppm_file << std::to_string(blue) << '\n';
//      ppm_file << red << ' ';
//      ppm_file << green << ' ';
//      ppm_file << blue << '\n';
    }

    ppm_file.close();
//    for(int i = 0; i < pixels.size(); i++)
//    {
//      pixels[i] = 127;
//    }
//    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels.data());
    colorSource->unbind();
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
