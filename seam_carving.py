import numpy as np
import cv2

class SeamCarver:
    def __init__(self, filename, out_height, out_width):
        self.filename = filename
        self.out_height = out_height
        self.out_width = out_width
        
        # Read image and initialize
        self.in_image = cv2.imread(filename).astype(np.float64)
        self.in_height, self.in_width = self.in_image.shape[:2]
        self.out_image = np.copy(self.in_image)
        
        # Seam tracking matrices
        self.seams_history = []
        self.col_shift = np.zeros((self.in_height, self.in_width), dtype=np.int32)
        self.row_shift = np.zeros((self.in_width, self.in_height), dtype=np.int32)
        
        # Forward energy kernels
        self.kernel_x = np.array([[0., 0., 0.], [-1., 0., 1.], [0., 0., 0.]], dtype=np.float64)
        self.kernel_y_left = np.array([[0., 0., 0.], [0., 0., 1.], [0., -1., 0.]], dtype=np.float64)
        self.kernel_y_right = np.array([[0., 0., 0.], [1., 0., 0.], [0., -1., 0.]], dtype=np.float64)
        
        self.seams_carving()

    def seams_carving(self):
        delta_row = int(self.out_height - self.in_height)
        delta_col = int(self.out_width - self.in_width)

        # Process vertical seams first
        if delta_col < 0:
            self.seams_removal(-delta_col, is_vertical=True)

        # Process horizontal seams
        if delta_row < 0:
            self.seams_removal(-delta_row, is_vertical=False)

    def _record_seam(self, seam_idx, is_vertical):
        original_seam = []
        if is_vertical:
            for row, col in enumerate(seam_idx):
                original_col = col + self.col_shift[row, col]
                original_seam.append((row, original_col))
                self.col_shift[row, original_col+1:] += 1
        else:
            rotated_image = self.rotate_image(self.out_image)
            for rot_row, rot_col in enumerate(seam_idx):
                original_row = rot_col + self.row_shift[rot_row, rot_col]
                original_col = self.in_height - 1 - rot_row
                original_seam.append((original_row, original_col))
                self.row_shift[rot_row, rot_col+1:] += 1
        self.seams_history.append(original_seam)

    def seams_removal(self, num_pixel, is_vertical):
        for _ in range(num_pixel):
            if is_vertical:
                energy_map = self.calc_energy_map()
                cumulative_map = self.cumulative_map_forward(energy_map, self.out_image)
                seam_idx = self.find_seam(cumulative_map)
                self._record_seam(seam_idx, True)
                self.delete_seam(seam_idx)
            else:
                rotated_image = self.rotate_image(self.out_image)
                energy_map = self.calc_energy_map(rotated_image)
                cumulative_map = self.cumulative_map_forward(energy_map, rotated_image)
                seam_idx = self.find_seam(cumulative_map)
                self._record_seam(seam_idx, False)
                self.delete_seam_rotated(seam_idx)

    def calc_energy_map(self, image=None):
        img = image if image is not None else self.out_image
        b, g, r = cv2.split(img)
        return np.absolute(cv2.Scharr(b, -1, 1, 0)) + np.absolute(cv2.Scharr(b, -1, 0, 1)) + \
               np.absolute(cv2.Scharr(g, -1, 1, 0)) + np.absolute(cv2.Scharr(g, -1, 0, 1)) + \
               np.absolute(cv2.Scharr(r, -1, 1, 0)) + np.absolute(cv2.Scharr(r, -1, 0, 1))

    def cumulative_map_forward(self, energy_map, image):
        matrix_x = self.calc_neighbor_matrix(self.kernel_x, image)
        matrix_y_left = self.calc_neighbor_matrix(self.kernel_y_left, image)
        matrix_y_right = self.calc_neighbor_matrix(self.kernel_y_right, image)

        m, n = energy_map.shape
        output = np.copy(energy_map)
        
        for row in range(1, m):
            for col in range(n):
                if col == 0:
                    costs = [
                        output[row-1, col+1] + matrix_x[row-1, col+1] + matrix_y_right[row-1, col+1],
                        output[row-1, col] + matrix_x[row-1, col]
                    ]
                elif col == n-1:
                    costs = [
                        output[row-1, col-1] + matrix_x[row-1, col-1] + matrix_y_left[row-1, col-1],
                        output[row-1, col] + matrix_x[row-1, col]
                    ]
                else:
                    costs = [
                        output[row-1, col-1] + matrix_x[row-1, col-1] + matrix_y_left[row-1, col-1],
                        output[row-1, col] + matrix_x[row-1, col],
                        output[row-1, col+1] + matrix_x[row-1, col+1] + matrix_y_right[row-1, col+1]
                    ]
                output[row, col] += np.min(costs)
        return output

    def calc_neighbor_matrix(self, kernel, image):
        b, g, r = cv2.split(image)
        return np.absolute(cv2.filter2D(b, -1, kernel=kernel)) + \
               np.absolute(cv2.filter2D(g, -1, kernel=kernel)) + \
               np.absolute(cv2.filter2D(r, -1, kernel=kernel))

    def find_seam(self, cumulative_map):
        m, n = cumulative_map.shape
        seam = np.zeros(m, dtype=np.uint32)
        seam[-1] = np.argmin(cumulative_map[-1])
        for row in range(m-2, -1, -1):
            col = seam[row+1]
            seam[row] = np.argmin(cumulative_map[row, max(col-1, 0):min(col+2, n)]) + max(col-1, 0)
        return seam

    def delete_seam(self, seam_idx):
        m, n = self.out_image.shape[:2]
        self.out_image = np.array([np.delete(row, seam_idx[i], axis=0) for i, row in enumerate(self.out_image)])

    def delete_seam_rotated(self, seam_idx):
        rotated = self.rotate_image(self.out_image)
        rotated = np.array([np.delete(row, seam_idx[i], axis=0) for i, row in enumerate(rotated)])
        self.out_image = self.rotate_image(rotated)

    def rotate_image(self, image):
        return np.rot90(image, 1, (0, 1))

    def save_seams_visualization(self, output_path):
        original = cv2.imread(self.filename)
        for seam in self.seams_history:
            for x, y in seam:
                if 0 <= x < original.shape[0] and 0 <= y < original.shape[1]:
                    original[x, y] = [0, 0, 255]
        cv2.imwrite(output_path, original)

    def save_result(self, filename):
        cv2.imwrite(filename, self.out_image.astype(np.uint8))