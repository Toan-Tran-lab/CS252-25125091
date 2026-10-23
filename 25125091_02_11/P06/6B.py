n, m, target = input().split()
m = int(m)
n = int(n)
direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
grid = []
map = {}
cnt = set()
for i in range(n):
    row = input()
    grid.append(row)
    
for r in range(n):
    for c in range(m):
        if grid[r][c] != target: continue
        for dr, dc in direction:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] != '.' and grid[nr][nc] != target: 
                cnt.add(grid[nr][nc])

print(len(cnt))