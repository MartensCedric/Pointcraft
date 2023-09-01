//
// Created by cedric on 8/23/23.
//
#pragma once
#include "PostProcessEffect.h"

class Bayer4by4 : public PostProcessEffect {

public:
  Bayer4by4(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/bayer4by4"),
                          enabled) {}

  void renderGui() override {
    ImGui::Checkbox("Enable Bayer 4x4 effect", &enabled);

  }

  void update() override {
    shader->setFloat("screen_width", 1600.f);
    shader->setFloat("screen_height", 900.f);
  }
};

