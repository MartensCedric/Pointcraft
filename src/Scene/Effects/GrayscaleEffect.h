//
// Created by cedric on 8/23/23.
//
#pragma once
#include "PostProcessEffect.h"

class GrayscaleEffect : public PostProcessEffect {

public:
  GrayscaleEffect(bool enabled)
      : PostProcessEffect(AssetManager::instance().loadShaderProgram("assets/shaders/grayscale"),
                          enabled) {}

  void renderGui() override {
    ImGui::Checkbox("Enable Grayscale effect", &enabled);

  }

  void update() override {
  }
};

