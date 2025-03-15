from seam_carving import SeamCarver
import os

def image_resize(filename_input, filename_output, new_height, new_width, visualize_seams_path):
    obj = SeamCarver(filename_input, new_height, new_width)
    obj.save_result(filename_output)
    obj.save_seams_visualization(visualize_seams_path)

if __name__ == '__main__':
    """
    Put the input image in the 'in/images' folder.
    The output resized image and seams visualization will be saved in 'out/images'.
    """

    folder_in = 'in'
    folder_out = 'out'

    filename_input = 'test6.jpg' 
    filename_output = 'image_result.png'
    visualize_seams = 'seams_visualization.png'
    new_height = 250
    new_width = 400

    input_image = os.path.join(folder_in, "images", filename_input)
    output_image = os.path.join(folder_out, "images", filename_output)
    output_seams = os.path.join(folder_out, "images", visualize_seams)

    image_resize(input_image, output_image, new_height, new_width, output_seams)
