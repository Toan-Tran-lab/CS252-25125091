s = input()
e = input()
x = ord(s[0]) - ord(e[0])
y = ord(s[1]) - ord(e[1])
diag = ('R' if x < 0 else 'L') + ('U' if y < 0 else 'D')
horizontal = ('R' if x < 0 else 'L')
vertical = ('U' if y < 0 else 'D')
x = abs(x)
y = abs(y)

if x > 0 and y > 0:
    print(min(x, y) + abs(x - y))
    for i in range(min(x, y)): print(diag)
    for i in range(abs(x - y)): print(horizontal if x > y else vertical)
else:
    print(x if x > y else y)
    for i in range(max(x,y)): print(horizontal if x > y else vertical)