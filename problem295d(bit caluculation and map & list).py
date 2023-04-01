# S = input()
# l = len(S)
# k = 0
# for i in range(l):
#     for j in range(l):
#         if i >= j:
#             pass
#         else:
#             w = []
#             for i2 in range(10):
#                 kosuu = S.count("i2", i, j + 1) % 2
#                 w.append(kosuu)
#             if w.count(0) == 10:
#                 k = k + 1
#             else:
#                 pass
# print(k)


# 自分の回答1(実行時間over)
# S = input()
# l = len(S)
# k = 0
# for i in range(l):
#     for j in range(l):
#         if i >= j:
#             pass
#         else:
#             w = []
#             kosuu = S.count("0", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("1", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("2", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("3", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("4", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("5", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("6", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("7", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("8", i, j + 1) % 2
#             w.append(kosuu)
#             kosuu = S.count("9", i, j + 1) % 2
#             w.append(kosuu)
#             if w.count(0) == 10:
#                 k = k + 1
#             else:
#                 pass
# print(k)

# 自分の回答2
# S = input()
# k = 0
# for i in range(len(S)):
#     for j in range(len(S)):
#         if i < j:
#             w = []
#             for i2 in range(10):
#                 t = str(i2)
#                 kosuu = S.count(t, i, j + 1) % 2
#                 w.append(kosuu)
#             if w.count(0) == 10:
#                 k = k + 1
# print(k)

# 自分の回答3
# s = input()
# hako = []
# for i in range(len(s) + 1):
#     w = []
#     for i2 in range(10):
#         i2 = str(i2)
#         kosuu = s[0:i].count(i2) % 2
#         w.append(kosuu)
#         res = "".join(map(str, w))
#     hako.append(res)
# import collections
# c = collections.Counter(hako)
# teki =c.most_common()
# values, counts =zip(*teki)
# ans = 0
# values = map(int,counts)
# for i in counts:
#     ans += i * (i-1) //2
# print(ans)






# 模範回答
s = list(map(int, list(input())))
counts = [0] * 1024
counts[0] = 1
tmp = 0
for i in range(len(s)):
    tmp ^= 1 << s[i]
    counts[tmp] += 1

ans = 0
for x in counts:
    ans += x * (x - 1) // 2
print(ans)

# https://www.javadrive.jp/python/num/index4.html
# bit演算に関する演算子



