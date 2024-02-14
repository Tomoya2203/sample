# 画像の一部分をトリミングしてOCRを行うプログラム

import cv2
import numpy as np
from google.cloud import vision
from google.oauth2 import service_account
import io
import os

win_name = 'disp'
out_image_fname = 'trim.jpg'


# clip x, y
def clipXY(x, y, img):
    rows, cols = img.shape[0:2]
    x = x if x > 0 else 0
    x = x if x <= cols else cols - 1
    y = y if y > 0 else 0
    y = y if y <= rows else rows - 1
    return x, y


# redraw
def redraw(x0, y0, x1, y1, color):
    global img
    imgDisp = img.copy()
    x1, y1 = clipXY(x1, y1, img)
    cv2.rectangle(imgDisp, (x0, y0), (x1, y1), color, 1)
    cv2.imshow(win_name, imgDisp)
    return x1, y1


# mouse Events
def mouseEvents(event, x, y, flags, param):
    global ix, iy, ex, ey, drawing, img
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            ex, ey = redraw(ix, iy, x, y, (0, 0, 255))
    elif event == cv2.EVENT_LBUTTONUP:
        ex, ey = redraw(ix, iy, ex, ey, (255, 0, 255))
        drawing = False


# triming
def trim(img, x0, y0, x1, y1):
    if x1 < x0:
        x0, x1 = x1, x0  # swap it
    if y1 < y0:
        y0, y1 = y1, y0  # swap it
    dst = img[y0:y1, x0:x1]  # trim
    cv2.imwrite(out_image_fname, dst)
    return dst


def doOcr():
    # 身元証明書のjson読み込み
    credentials = service_account.Credentials.from_service_account_file('key.json')
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # 読み込む画像データの指定
    with io.open(out_image_fname, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.document_text_detection(
        image=image,
        image_context={'language_hints': ['ja']})

    output_text = ''
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    output_text += ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                output_text += '\n'
    print(output_text)


if __name__ == "__main__":
    img = cv2.imread("/Users/ooyamatomoya/PycharmProjects/pythonProject/Isogawa_lab/test_picture/IMG_20231219_0074.jpg")  # read image

    drawing = False
    cv2.namedWindow(win_name)
    cv2.setMouseCallback(win_name, mouseEvents)
    cv2.imshow(win_name, img)
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("o"):
            trimImg = trim(img, ix, iy, ex, ey)
            doOcr()
            cv2.imshow('trim', trimImg)
            continue

    cv2.destroyAllWindows()
