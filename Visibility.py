import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import _structural_similarity as ssim
import cv2


def getVisibility(imgPath, logoPath, logo_sides):
    """Compare the visibility using ssim"""
    logo_B = cv2.imread(logoPath)
    img_B = cv2.imread(imgPath)

    img_B = img_B[logo_sides["top"]:logo_sides["bottom"],
    logo_sides["left"]:logo_sides["right"]].copy()

    logo_B = cv2.cvtColor(logo_B, cv2.COLOR_BGR2GRAY)
    img_B = cv2.cvtColor(img_B, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Crop Test", img_B)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return 1 - ssim.compare_ssim(logo_B, img_B)


if __name__ == '__main__':
    print(getVisibility('./input/DSC_0004.jpg', 'logo.png', {"top": 0, "bottom": 75, "left": 0, "right": 300}))
