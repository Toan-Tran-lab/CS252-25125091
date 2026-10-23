t, n = map(int, input().split())
x = 1
arr = [0] * n
for k in range(t):
    cmd = input()
    if cmd[0] == 'a':
        size = int(cmd.split()[1])
        s, e, exist = -1, -1, 0
        for i in range(n):
            if arr[i] != 0: s, e = -1, -1
            elif s == -1: s = e = i
            else: e = i
            if s != -1 and e - s + 1 >= size:
                exist = 1
                break 
        if exist == 0: 
            print("NULL")
            continue
        for i in range(size): arr[s + i] = x
        print(x)
        x += 1
    elif cmd[0] == 'e':
        identifier = int(cmd.split()[1])
        exist = 0
        for i in range(n):
            if arr[i] == identifier:
                arr[i] = 0
                exist = 1
        if (identifier <= 0 or exist == 0):
            print("ILLEGAL_ERASE_ARGUMENT")
    else:
        a, b = 0, 0
        while b < n:
            while b < n and arr[b] == 0: b += 1
            if b == n: break
            arr[a], arr[b] = arr[b], arr[a]
            a += 1
            b += 1