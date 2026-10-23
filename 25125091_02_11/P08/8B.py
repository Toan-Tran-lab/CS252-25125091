import sys
move = input()
x, y, px, py = 0, 0, 0, 0
visited = set([(0, 0)])
direction = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
for c in move:
    if c == 'R': x += 1
    elif c == 'L': x -= 1
    elif c == 'U': y += 1
    elif c == 'D': y -= 1
    for dx, dy in direction:
        nx, ny = x + dx, y + dy
        if (nx != px or ny != py) and (nx, ny) in visited:
            print("BUG")
            sys.exit()
    px, py = x, y
    visited.add((x, y))
print("OK")