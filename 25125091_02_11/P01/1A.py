import math
m, n, x = map(int, input().split())
print(math.ceil(m / x) * math.ceil(n / x))
