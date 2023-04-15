import cv2


def flip_horizontal(img: cv2.Mat) -> cv2.Mat:
    return cv2.flip(img, 1)


def flip_vertical(img: cv2.Mat) -> cv2.Mat:
    return cv2.flip(img, 0)


def invert_colors(img: cv2.Mat) -> cv2.Mat:
    return 255 - img # vectorization


def blur(img: cv2.Mat) -> cv2.Mat:
    kernel = (13, 13) # average filter with 13x13 kernel
    return cv2.blur(img, kernel)


def edge_detect(img: cv2.Mat) -> cv2.Mat:
    # == Laplace ==
    ddepth = cv2.CV_16S
    kernel_size = 3
    filteredImg = cv2.GaussianBlur(img, (3,3), 0)
    gray_img = cv2.cvtColor(filteredImg, cv2.COLOR_BGR2GRAY)
    processedImg = cv2.Laplacian(gray_img, ddepth, ksize=kernel_size)
    abs_img = cv2.convertScaleAbs(processedImg)
    return abs_img

    # == Canny ==
    # return cv2.Canny(img,125,175)


def draw_contours(img: cv2.Mat) -> cv2.Mat:
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgGray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cv2.drawContours(img, contours, -1, (0,255,0), 3) # green contours on original img


def transform(img: cv2.Mat, operations: list[str]) -> cv2.Mat:

    result = img.copy()
    for operation in operations:

        match operation:

            case 'flip_horizontal':
                result = flip_horizontal(result)
            case 'flip_vertical':
                result = flip_vertical(result)
            case 'invert_colors':
                result = invert_colors(result)
            case 'blur':
                result = blur(result)
            case 'edge_detect':
                result = edge_detect(result)
            case 'draw_contours':
                result = draw_contours(result)
            case _:
                print(f"Operation '{operation}' not supported, skipping...")

    return result