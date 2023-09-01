//
// Created by cedric on 8/23/23.
//
#pragma once
#include "PostProcessEffect.h"

class Bayer8by8 : public PostProcessEffect {

public:
  Bayer8by8(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/bayer8by8"),
                          enabled) {}

  void renderGui() override {
    ImGui::Checkbox("Enable Bayer 8x8 effect", &enabled);

  }

  void update() override {
    shader->setFloat("screen_width", 1600.f);
    shader->setFloat("screen_height", 900.f);
  }
};

