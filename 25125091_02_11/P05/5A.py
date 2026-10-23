import sys
total = 0
chat = set()
for line in sys.stdin:
    line = line.strip()
    if not line: break
    if line[0] == '+': chat.add(line[1:])
    elif line[0] == '-': chat.discard(line[1:])
    else: total += len(line.split(':', 1)[1]) * len(chat)
print(total)