N = int(input())
lis = [None] * 100
lis[0] = "F"
lis[1] = "FLF"
if N == 0:
    print("F")
if N == 1:
    print("FLF")
for i in range(2,N + 1):
    rev = lis[i-1][::-1]
    rev =rev.replace("L", "X")
    rev = rev.replace("R", "L")
    rev =rev.replace("X", "R")
    lis[i] = lis[i-1] + "L" + rev
    if i == N:
        print(lis[i])
        exit()

