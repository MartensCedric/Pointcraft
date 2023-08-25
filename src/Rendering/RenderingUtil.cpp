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


void down_sample(const std::vector<uint8_t>& input, std::vector<uint8_t>& output, int width, int height, int sample_width, int sample_height)
{
  int new_width = width / sample_width;
  int new_height = height / sample_height;
  int samples_per_pixel = sample_width * sample_height;
  for(int x = 0; x < new_width; x++)
  {
    for(int y = 0; y < new_height; y++)
    {
      int acc_red = 0;
      int acc_green = 0;
      int acc_blue = 0;

      // take into account colors when up/down sampling
      int new_index = get_index(x, y, new_width);

      for(int i = 0; i < sample_width; i++)
      {
        for(int j = 0; j < sample_height; j++)
        {
          int old_x = sample_width * x + i;
          int old_y = sample_height * y + j;
          int index = get_index(old_x, old_y, width);
          acc_red += input[index*4];
          acc_green += input[index*4+1];
          acc_blue += input[index*4+2];
        }
      }

      output[new_index*4] = acc_red / samples_per_pixel;
      output[new_index*4+1] = acc_green / samples_per_pixel;
      output[new_index*4+2] = acc_blue / samples_per_pixel;
    }
  }
}

void up_sample(const std::vector<uint8_t>& input, std::vector<uint8_t>& output, int width, int height, int sample_width, int sample_height) {
  int old_width = width / sample_width;
  int old_height = height / sample_height;
  int samples_per_pixel = sample_width * sample_height;
  for(int x = 0; x < width; x++) {
    for(int y = 0; y < height; y++) {
      int index = get_index(x, y, width);
      int old_index = get_index(x / sample_width, y / sample_height, old_width);
      output[index*4] = input[old_index*4];
      output[index*4+1] = input[old_index*4+1];
      output[index*4+2] = input[old_index*4+2];
      output[index*4+3] = 255;
    }
  }
}

int get_index(int x, int y, int width)
{
  return y*width + x;
}
