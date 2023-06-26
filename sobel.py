import cv2
import numpy as np


# def applyFilter(img, filt):
#     # 入力画像のサイズ取得
#     img_row = img.shape[0]
#     img_col = img.shape[1]
#
#     # フィルタのサイズ取得 (適さないフィルタサイズの場合はエラーを返す)
#     filt_row = filt.shape[0]
#     filt_col = filt.shape[1]
#     if (filt_row % 2 == 0) or (filt_col % 2 == 0):
#         print("フィルタサイズ設定に誤りがあります。")
#         return img
#
#     # 結果画像初期化
#     result_img = np.zeros((img_row, img_col))
#
#     # フィルタの中心部分算出
#     filt_mid = int(filt_row / 2)
#
#     # フィルタ適用
#     for row in range(img_row):
#         for col in range(img_col):
#             if (row - 3 < 0) or (col - 3 < 0) or ((row + 3 >= img_row)) or (
#                     (col + 3 >= img_col)):
#                 continue  # 端の画素は無視 (画素値0)
#             tmp_result = img[row - filt_mid:row + filt_mid + 1, col - filt_mid:col + filt_mid + 1]  # 計算に使う周りの画素取得
#
#             tmp_result = tmp_result * filt
#             result_img[row, col] = round(np.sum(tmp_result))
#
#     return result_img


img = cv2.imread('../../../Pictures/gray_img.jpg')
kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])


# cv2.imwrite('frame_canny2.jpg', applyFilter(img, kernel_x))

def filter2d(ndarray, kernel):
    a = ndarray.shape[0]
    b = ndarray.shape[1]
    result = np.zeros((a - 2, b - 2))
    for i in range(a - 2):
        for j in range(b - 2):
            one = kernel[0][0] * ndarray[i][j][0] + kernel[1][0] * ndarray[i + 1][j][0] + kernel[2][0] * \
                  ndarray[i + 2][j][0]
            sec = kernel[0][1] * ndarray[i][j + 1][0] + kernel[1][1] * ndarray[i + 1][j + 1][0] + \
                  kernel[2][1] * ndarray[i + 2][j + 1][0]
            thi = kernel[0][2] * ndarray[i][j + 2][0] + kernel[1][2] * ndarray[i + 1][j + 2][0] + \
                  kernel[2][2] * ndarray[i + 2][j + 2][0]
            result[i][j] = one + sec + thi
    return result

def gradient_magnitude(sobel_x, sobel_y):
    a = sobel_x.shape[0]
    b = sobel_x.shape[1]
    result = np.zeros((a - 2, b - 2))
    for i in range(a - 2):
        for j in range(b - 2):
            c = (sobel_x[i][j] ** 2 + sobel_y[i][j] ** 2) ** 0.5
            if c < 255:
                result[i][j] = c
            else:
                result[i][j] = 255
    result = result.astype(np.uint8)
    return result


cv2.imwrite('gray3.jpg', gradient_magnitude(filter2d(img, kernel_x), filter2d(img,kernel_y)))


