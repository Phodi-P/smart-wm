from PIL import Image
import numpy

def getBrightness(img):
    """Returns 2d list of brightness calculated from each pixel"""
    pixel_access = img.load()
    brightness = numpy.zeros(img.size)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pix = pixel_access[x,y]
            Y = (0.375 * pix[0] + 0.5 * pix[1] + 0.125 * pix[2])
            if len(pix) > 3:
                percent = pix[3]/255
                Y *= percent
            brightness[x,y] = Y
    del img
    return brightness

def getVisibility(img, logoBrightness, logo_sides):
    """Compare the brightness value of each pixel and average it out"""
    logo_B = logoBrightness
    img_B = getBrightness(img)

    avg_diff = 0
    for x in range(logo_sides["size"][0]):
        for y in range(logo_sides["size"][1]):
            diff = abs(logo_B[x,y]-img_B[logo_sides["left"]+x,logo_sides["top"]+y])
            avg_diff += diff
    avg_diff /= logo_sides["size"][0]*logo_sides["size"][1]
    avg_diff *= 100/255
    avg_diff = 100-avg_diff
    return avg_diff