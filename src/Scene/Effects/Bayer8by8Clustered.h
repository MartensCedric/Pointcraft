//
// Created by cedric on 8/23/23.
//
#pragma once
#include "PostProcessEffect.h"

class Bayer8by8Clustered : public PostProcessEffect {

public:
  Bayer8by8Clustered(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/bayer8by8_cluster"),
                          enabled) {}

  void renderGui() override {
    ImGui::Checkbox("Enable Bayer 8x8 Clustered effect", &enabled);

  }

  void update() override {
    shader->setFloat("screen_width", 1600.f);
    shader->setFloat("screen_height", 900.f);
  }
};

