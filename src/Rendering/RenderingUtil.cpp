//
// Created by cedric on 8/24/23.
//

#include "RenderingUtil.h"
#include <iostream>
#include <fstream>

void pixels_to_ppm(const std::vector<uint8_t>& data, int width, int height, const std::string& filename)
{
  std::ofstream ppm_file(filename, std::ios::binary);
  if (!ppm_file.is_open()) {
    std::cerr << "Error opening file: " << filename<< std::endl;
    return;
  }

  ppm_file << "P3\n" << width << " " << height << "\n255\n";

  for(int i = 0; i < width*height; i++)
  {
    uint8_t red = data[i * 4];
    uint8_t green = data[i * 4 + 1];
    uint8_t blue = data[i * 4 + 2];

    ppm_file << std::to_string(red) << ' ';
    ppm_file << std::to_string(green) << ' ';
    ppm_file << std::to_string(blue) << '\n';
  }

  ppm_file.close();
}
