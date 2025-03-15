# Seam Carving
Seam Carving for Content Aware Image Resizing and Object Removal


## Algorithm Overview
### Seam Removal
1. Calculate energy map: 
>Energy is calculated by sum the absolute value of the gradient in both x direction and y direction for all three channel (B, G, R). Energy map is a 2D image with the same dimension as input image.

2. Build accumulated cost matrix using forward energy: 
>This step is implemented with dynamic programming. The value of each pixel is equal to its corresponding value in the energy map added to the minimum new neighbor energy introduced by removing one of its three top neighbors (top-left, top-center, and top-right)

3. Find and remove minimum seam from top to bottom edge: 
>Backtracking from the bottom to the top edge of the accumulated cost matrix to find the minimum seam. All the pixels in each row after the pixel to be removed are shifted over one column to the left if it has index greater than the minimum seam.

4. Repeat step 1 - 3 until achieving targeting width 

5. Rotate image and repeat step 1 - 4 for vertical resizing: 
>Rotating image 90 degree counter-clockwise and repeat the same steps to remove rows.
