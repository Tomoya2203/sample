import os
import json
import glob
import cv2


# 画像領域をtrimする
def trim(img, x0, y0, x1, y1):
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    dst = img[y0:y1, x0:x1]
    cv2.imwrite('trim.jpg', dst)
    return dst


# 100分率をpixelに変換する関数
def convert_from_ls(x, y, width, height, original_width, original_height):
    pixel_x = x / 100.0 * original_width
    pixel_y = y / 100.0 * original_height
    pixel_width = width / 100.0 * original_width
    pixel_height = height / 100.0 * original_height
    return int(pixel_x), int(pixel_y), int(pixel_x + pixel_width), int(pixel_y + pixel_height)


# current directoryの取得
current_directory = os.getcwd()
# 各文字に数字を割り振る
dic = {'ｲ一': 1, '仁': 2, 'ｲ三': 3, 'ｲ四': 4, '伍': 5, 'ｲ六': 6, 'ｲ七': 7, 'ｲ八': 8, 'ｲ九': 9, 'ｲ一・': 10, '仁・': 11,
       'ｲ三・': 12, 'ｲ四・': 13, '伍・': 14, 'ｲ六・': 15, 'ｲ七・': 16, 'ｲ八・': 17, 'ｲ九・': 18, '一': 19, '二': 20, '三': 21,
       '四': 22, '五': 23, '六': 24, '七': 25, '八': 26, '九': 27, '一・': 28, '二・': 29, '三・': 30, '四・': 31,
       '五・': 32, '六・': 33, '七・': 34, '八・': 35, '九・': 36, '1': 37, '2': 38, '3': 39, '4': 40, '5': 41, '6': 42,
       '7': 43, '8': 44, '9': 45, '1・': 46, '2・': 47, '3・': 48, '4・': 49, '5・': 50, '6・': 51, '7・': 52, '8・': 53,
       '9・': 54, '◯': 55, '◎': 56, '△': 57, '△・': 58, 'ス': 59, '^': 60, 'スリ上': 61, 'スリ下': 62, 'スリ上下': 63, '々': 64,
       'く': 65, 'ウ': 66}
# 各文字が何個含まれるか
num = {'ｲ一': 0, '仁': 0, 'ｲ三': 0, 'ｲ四': 0, '伍': 0, 'ｲ六': 0, 'ｲ七': 0, 'ｲ八': 0, 'ｲ九': 0, 'ｲ一・': 0, '仁・': 0,
       'ｲ三・': 0, 'ｲ四・': 0, '伍・': 0, 'ｲ六・': 0, 'ｲ七・': 0, 'ｲ八・': 0, 'ｲ九・': 0, '一': 0, '二': 0, '三': 0, '四': 0,
       '五': 0, '六': 0, '七': 0, '八': 0, '九': 0, '一・': 0, '二・': 0, '三・': 0, '四・': 0, '五・': 0, '六・': 0,
       '七・': 0, '八・': 0, '九・': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '1・': 0,
       '2・': 0, '3・': 0, '4・': 0, '5・': 0, '6・': 0, '7・': 0, '8・': 0, '9・': 0, '◯': 0, '◎': 0, '△': 0, '△・': 0, 'ス': 0,
       '^': 0, 'スリ上': 0, 'スリ下': 0, 'スリ上下': 0, '々': 0, 'く': 0, 'ウ': 0}

# 画像を分類するdirectoryの作成。directoryが存在すると動かないので注意
for i in dic.values():
    os.makedirs(current_directory + '/' + str(i))

# jsonファイルの取得
json_file = glob.glob(current_directory + '/*.json')
with open(json_file[0]) as f:
    data = json.load(f)
# print(data[0])

for i in data:
    # 大元の画像ファイルの取得
    picture_name = i['file_upload']
    line = picture_name.find('-')
    picture_name = picture_name[line + 1:]
    img = cv2.imread(current_directory + '/' + picture_name)

    # 大元の画像ファイル名とその画像を表示する
    # print(picture_name)
    # cv2.imshow('Image2', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    for j in i['annotations']:
        for k in j['result']:
            label = k['value']['rectanglelabels'][0]
            # 長さが100分率となっているのでpixelに変換する
            x0, y0, x1, y1 = convert_from_ls(k['value']['x'], k['value']['y'],
                                             k['value']['width'], k['value']['height'],
                                             k['original_width'], k['original_height'])

            # 保存するファイル名と%で表した縦横の長さ、pixelで表した縦横の長さの出力
            # 2つ目のprintで一つでも100を超えていたらエラーが出る。その時はlabel studioでのアノテーションが間違っている
            # print(current_directory + '/' + str(dic[label]) +
            #             '/' + str(dic[label]) + '_' + str(num[label]) + '.jpg')
            # print(k['value']['x'], k['value']['y'], k['value']['width'], k['value']['height'],
            #       k['original_width'], k['original_height'])
            # print(x0, y0, x1, y1)

            # 画像をトリミングして保存
            cut = trim(img, x0, y0, x1, y1)
            cv2.imwrite(current_directory + '/' + str(dic[label]) +
                        '/' + str(dic[label]) + '_' + str(num[label]) + '.jpg', cut)
            num[label] += 1

            # 切り取った画像の表示
            # cv2.imshow('Image2', cut)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()


