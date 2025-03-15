# Seam Carving with Forward Energy

This repository contains a Python implementation of the **Seam Carving** algorithm using **Forward Energy** for content-aware image resizing. Seam carving is a technique that resizes images by removing or inserting seams (connected paths of pixels) that are least noticeable. This implementation supports both vertical and horizontal seam removal and includes visualization of the removed seams.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Usage](#usage)
5. [How It Works](#how-it-works)
6. [Example](#example)
7. [Visualization](#visualization)
8. [License](#license)

---

## Introduction

Seam carving is an algorithm for content-aware image resizing. Unlike traditional resizing methods that uniformly scale or crop an image, seam carving removes or inserts seams (paths of least importance) to preserve the most important features of the image. This implementation uses **forward energy** to minimize visual artifacts during seam removal.

---

## Features

- **Seam Removal**: Remove seams in both vertical and horizontal directions.
- **Forward Energy**: Uses forward energy to calculate the optimal seams for removal.
- **Seam Visualization**: Visualize the removed seams on the original image.
- **Image Resizing**: Resize images to target dimensions while preserving important content.

---

## Requirements

To run this code, you need the following Python libraries:

- `numpy`
- `opencv-python`
- `matplotlib`

You can install the required libraries using pip:

```bash
pip install numpy opencv-python matplotlib
```

---

## Usage

1. Clone the repository or download the `.ipynb` file.
2. Open the Jupyter Notebook or Python script.
3. Modify the `image_path` variable to point to your desired image.
4. Set the target dimensions (`target_width` and `target_height`) for resizing.
5. Run the script to resize the image and visualize the removed seams.

---

## How It Works

1. **Energy Map Calculation**: The energy map is calculated using the gradient magnitude of the image.
2. **Cumulative Energy Map**: A cumulative energy map is computed using forward energy to determine the optimal seams.
3. **Seam Removal**: Seams are removed iteratively based on the cumulative energy map.
4. **Seam Visualization**: The removed seams are visualized on the original image for better understanding.

---

## Example

Here’s an example of how to use the `SeamCarver` class:

```python
# Import the SeamCarver class
from seam_carving import SeamCarver

# Define the image path and target dimensions
image_path = "path_to_your_image.jpg"
target_width = 400  # Desired width
target_height = 300  # Desired height

# Create a SeamCarver instance
carver = SeamCarver(image_path, out_height=target_height, out_width=target_width)

# Save the resized image
carver.save_result("resized_image.jpg")

# Visualize the removed seams
vertical_vis, horizontal_vis = carver.visualize_seams(output_path="seams_visualization")
```

---

## Visualization

The script generates the following visualizations:

1. **Original Image**: The input image before resizing.
2. **Resized Image**: The image after seam carving.
3. **Vertical Seams**: Visualization of the removed vertical seams.
4. **Horizontal Seams**: Visualization of the removed horizontal seams.

## Example output:

![Example 1](https://raw.githubusercontent.com/sally-z10/Seam-Carving/main/example%201.jpg)
![Example 2](https://raw.githubusercontent.com/sally-z10/Seam-Carving/main/example%202.png)



---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- The algorithm is based on the original paper by Shai Avidan and Ariel Shamir: ["Seam Carving for Content-Aware Image Resizing"](https://dl.acm.org/doi/10.1145/1276377.1276390).
- Special thanks to the OpenCV and Matplotlib communities for their excellent libraries.

---

Feel free to contribute or report issues! 🚀
