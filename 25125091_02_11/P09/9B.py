import math
n, v_b, v_s = map(int, input().split())
arr = [int(x) for x in input().split()]
x_u, y_u = map(int, input().split())
minT = 1e9
minD = 1e9
res = -1
for i in range(1, n):
    d = math.sqrt((arr[i] - x_u) ** 2 + y_u ** 2)
    t = arr[i] / v_b + d / v_s
    if minT > t or (minT == t and minD > d):
        minT = t
        minD = d
        res = i
print(res + 1)