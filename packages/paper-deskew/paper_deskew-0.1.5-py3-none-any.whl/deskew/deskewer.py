from PIL import Image
import numpy as np
import argparse
import cv2
from skimage.transform import rotate
import time
import fast_histogram

class Deskewer():
    def __init__(self):
        self.thetas_step = 0.05
        self.min_theta = 85
        self.max_theta = 95
        self.num_rhos = 500

    def edge_detection(self, image):
        edge_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edge_image = cv2.GaussianBlur(edge_image, (3, 3), 1)
        edge_image = cv2.Canny(edge_image, 100, 200)
        edge_image = cv2.dilate(
            edge_image,
            cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
            iterations=1
        )

        edge_image = cv2.erode(
            edge_image,
            cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)),
            iterations=1
        )
        edge_image = edge_image[:-1] - edge_image[1:]
 
        return edge_image

    def deskew(self, image):
        image = image[:image.shape[0]//2]

        edge_image = self.edge_detection(image)       
        edge_height, edge_width = edge_image.shape[:2]
        edge_height_half, edge_width_half = edge_height / 2, edge_width / 2

        d = np.sqrt(np.square(edge_height) + np.square(edge_width))
        drho = (2 * d) / self.num_rhos

        thetas = np.arange(self.min_theta, self.max_theta, step=self.thetas_step)
        rhos = np.arange(-d, d, step=drho)

        cos_thetas = np.cos(np.deg2rad(thetas))
        sin_thetas = np.sin(np.deg2rad(thetas))

        accumulator = np.zeros((len(rhos), len(thetas)))

        edge_points = np.argwhere(edge_image != 0)
        edge_points = edge_points - np.array([[edge_height_half, edge_width_half]])
        rho_values = np.matmul(edge_points, np.array([sin_thetas, cos_thetas]))
#        accumulator, theta_vals, rho_vals = fast_histogram.histogram2d(
        accumulator  = fast_histogram.histogram2d(       
          np.tile(thetas, rho_values.shape[0]),
          rho_values.ravel(),
          range =[[self.min_theta, self.max_theta],[-d, d]],
         # bins=[thetas, rhos]
         bins=[len(thetas), len(rhos)]
        )

        accumulator = np.transpose(accumulator)
        max_line = np.unravel_index(accumulator.argmax(), accumulator.shape)

        theta = thetas[max_line[1]]
        rot_angle = theta - 90
        rotate_img = rotate(image, rot_angle, cval=255, resize=True, preserve_range=True)
        rotate_img = rotate_img.astype(np.uint8)        
        
        return rotate_img

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', required=True, help='path to pdf')
    args = parser.parse_args()
    
    deskewer = Deskewer()
    start = time.time()

    img = cv2.imread(args.img)
    img = deskewer.deskew(img)
    cv2.imwrite('./out.jpg', img)
    
    print(time.time()  - start)
if __name__ == '__main__':
    main()
