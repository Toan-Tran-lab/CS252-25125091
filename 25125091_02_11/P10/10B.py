import math

n, k = map(int, input().split())
arr = [int(x) for x in input().split()]
grid = [[0] * k for _ in range(k)]
c = math.floor(k / 2)

for w in arr:
    candidates = []
    for x in range(k):
        r = 0
        while r < k:
            while r < k and grid[x][r] == 1: r += 1
            l = r
            while r < k and grid[x][r] == 0:
                if r - l + 1 == w: 
                    candidates.append((x, l, r))
                    l += 1
                r += 1
    if not candidates: 
        print(-1)
        continue
    minD = 1e6
    minX = 1e6
    minL = 1e6
    for (x, l, r) in candidates:
        d = w * abs(x - c)
        if l <= c and r <= c: d += (c - l) * (c - l + 1) / 2 - (c - r) * (c - r - 1) / 2
        elif l > c and r > c: d += (r - c) * (r - c + 1) / 2 - (l - c - 1) * (l - c) / 2
        else: d += (c - l) * (c - l + 1) / 2 + (r - c) * (r - c + 1) / 2
        if minD > d or (minD == d and minX > x) or (minD == d and minX == x and minL > l):
            tx, tl, tr = x, l, r
            minD, minX, minL = d, x, l
    for i in range(tl, tr + 1): grid[tx][i] = 1
    print(str(tx + 1) + ' ' + str(tl + 1) + ' ' + str(tr + 1))