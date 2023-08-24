//
// Created by cedric on 8/24/23.
//

#ifndef POINT_CRAFT_RENDERINGUTIL_H
#define POINT_CRAFT_RENDERINGUTIL_H

#include <vector>
#include <stdint.h>
#include <string>

void pixels_to_ppm(const std::vector<uint8_t>& data, int width, int height, const std::string& filename);

template<typename gray_t>
void rgba_to_grayscale(const std::vector<uint8_t>& rgba, std::vector<gray_t>& grayscale)
{
  for(int i = 0; i < rgba.size() / 4; i++)
  {
      float red = static_cast<float>(rgba[i*4]);
      float green = static_cast<float>(rgba[i*4+1]);
      float blue = static_cast<float>(rgba[i*4+2]);
      grayscale[i] = static_cast<gray_t>(0.299f * red + 0.587f * green + 0.114 * blue);
  }
}

#endif  //POINT_CRAFT_RENDERINGUTIL_H
