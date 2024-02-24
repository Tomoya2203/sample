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

# 以下はテストで用いたコードなので無視してください
# i = {'id': 6, 'annotations': [{'id': 7, 'completed_by': 1, 'result': [
#     {'original_width': 2016, 'original_height': 2976, 'image_rotation': 0,
#      'value': {'x': 81.26922811352618, 'y': 7.415861955564806, 'width': 7.236301133396168, 'height': 1.8853886327707121,
#                'rotation': 0, 'rectanglelabels': ['二']}, 'id': '2GQdnRCcg0', 'from_name': 'label', 'to_name': 'image',
#      'type': 'rectanglelabels', 'origin': 'manual'},
#     {'original_width': 2016, 'original_height': 2976, 'image_rotation': 0,
#      'value': {'x': 80.898135747711, 'y': 13.072027853876946, 'width': 7.792939682118941, 'height': 2.3881589348429024,
#                'rotation': 0, 'rectanglelabels': ['一']}, 'id': '704U6Tr6qY', 'from_name': 'label', 'to_name': 'image',
#      'type': 'rectanglelabels', 'origin': 'manual'}],
#                                'was_cancelled': False, 'ground_truth': False,
#                                'created_at': '2024-02-23T07:37:12.743346Z',
#                                'updated_at': '2024-02-23T07:37:41.547686Z',
#                                'draft_created_at': '2024-02-23T07:34:39.641046Z', 'lead_time': 208.49599999999998,
#                                'prediction': {}, 'result_count': 0,
#                                'unique_id': '8d549e68-441a-4e18-a5d6-763289718917', 'import_id': None,
#                                'last_action': None, 'task': 6, 'project': 5, 'updated_by': 1,
#                                'parent_prediction': None, 'parent_annotation': None, 'last_created_by': None}],
#      'file_upload': 'bfbe3766-IMG_20231219_0052.jpg', 'drafts': [], 'predictions': [],
#      'data': {'image': '/data/upload/5/bfbe3766-IMG_20231219_0052.jpg'}, 'meta': {},
#      'created_at': '2024-02-23T06:35:19.792848Z', 'updated_at': '2024-02-23T07:37:41.566757Z', 'inner_id': 4,
#      'total_annotations': 1, 'cancelled_annotations': 0, 'total_predictions': 0, 'comment_count': 0,
#      'unresolved_comment_count': 0, 'last_comment_updated_at': None, 'project': 5, 'updated_by': 1,
#      'comment_authors': []}
#
# img = cv2.imread(current_directory + '/IMG_20231219_0052.jpg')
# for j in i['annotations']:
#     for k in j['result']:
#         label = k['value']['rectanglelabels'][0]
#         x0, y0, x1, y1 = convert_from_ls(k['value']['x'], k['value']['y'],
#                                          k['value']['width'], k['value']['height'],
#                                          k['original_width'], k['original_height'])
#         cut = trim(img, x0, y0, x1, y1)
#         cv2.imwrite(current_directory + '/' + dic[label] + '/' + dic[label] + '_' + dic[num])
#         dic[num] += 1
#         # # 画像の表示
#         # cv2.imshow('Image2', cut)
#         # # キー入力を待つ
#         # cv2.waitKey(0)
#         # # ウィンドウを閉じる
#         # cv2.destroyAllWindows()
