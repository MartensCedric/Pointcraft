//
// Created by cedric on 8/23/23.
//

#ifndef POINT_CRAFT_FLOYDSTEINBERGEFFECT_H
#define POINT_CRAFT_FLOYDSTEINBERGEFFECT_H

#include "PostProcessEffect.h"

class FloydSteinbergEffect : public PostProcessEffect {

public:
  FloydSteinbergEffect(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/floyd_steinberg"),
                          enabled) {}

  void renderGui() override {
    ImGui::Checkbox("Enable Floyd-Steinberg effect", &enabled);

//    if (enabled) {
//      ImGui::SliderFloat("Aberration start", &aberrationStart, 0.5, 3);
//      ImGui::SliderFloat("Aberration R Offset", &aberrationROffset, -0.01, 0.01);
//      ImGui::SliderFloat("Aberration G Offset", &aberrationGOffset, -0.01, 0.01);
//      ImGui::SliderFloat("Aberration B Offset", &aberrationBOffset, -0.01, 0.01);
//    }
  }

  void update() override {
//    shader->setFloat("start", aberrationStart);
//    shader->setFloat("rOffset", aberrationROffset);
//    shader->setFloat("gOffset", aberrationGOffset);
//    shader->setFloat("bOffset", aberrationBOffset);
  }
};

#endif  //POINT_CRAFT_FLOYDSTEINBERGEFFECT_H
