//
// Created by cedric on 8/23/23.
//
#pragma once
#include "PostProcessEffect.h"

class Bayer8by8Random : public PostProcessEffect {

public:
  Bayer8by8Random(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/bayer8by8_random"),
                          enabled) {}

  void renderGui() override {
    ImGui::Checkbox("Enable Bayer 8x8 Random effect", &enabled);

  }

  void update() override {
    shader->setFloat("screen_width", 1600.f);
    shader->setFloat("screen_height", 900.f);
  }
};

