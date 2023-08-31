//
// Created by cedric on 8/23/23.
//
#pragma once
#include "PostProcessEffect.h"

class Bayer2by2 : public PostProcessEffect {

public:
  Bayer2by2(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/bayer2by2"),
                          enabled) {}

  void renderGui() override {
    ImGui::Checkbox("Enable Bayer 2x2 effect", &enabled);

  }

  void update() override {
    shader->setFloat("screen_width", 1600.f);
    shader->setFloat("screen_height", 900.f);
  }
};

