import cv2

import os

target_size = 1280


def resize(path_image, out_path):
    im = cv2.imread(path_image)
    height, width = im.shape[:2]  # 取彩色图片的长、宽。

    ratio_h = height / target_size
    ration_w = width / target_size

    ratio = max(ratio_h, ration_w)

    # 缩小图像  resize(...,size)--size(width，height)
    size = (int(width / ratio), int(height / ratio))
    shrink = cv2.resize(im, size, interpolation=cv2.INTER_AREA)  # 双线性插值
    BLACK = [0, 0, 0]

    a = (target_size - int(width / ratio)) / 2
    b = (target_size - int(height / ratio)) / 2

    constant = cv2.copyMakeBorder(shrink, int(b), int(b), int(a), int(a), cv2.BORDER_CONSTANT, value=BLACK)
    constant = cv2.resize(constant, (target_size, target_size), interpolation=cv2.INTER_AREA)
    cv2.imwrite(out_path, constant, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    return constant


if __name__ == '__main__':
    directory_name = r"E:\Yolov5\historyStreet\historyStreet2\images"
    path_target = r"E:\Yolov5\historyStreet\historyStreet2\image"
    if not os.path.exists(path_target):
        os.makedirs(path_target)
    for picture_name in os.listdir(directory_name):
        file_name = directory_name + os.sep + picture_name  # 读取文件夹地址+图片名称类型
        resize(file_name, path_target+ os.sep + picture_name)
        print(file_name)
