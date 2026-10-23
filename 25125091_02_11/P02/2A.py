from collections import defaultdict

n = int(input())
rounds = []
finalScore = defaultdict(int)
for i in range(n):
    name, score = input().split()
    score = int(score)
    rounds.append([name, score])
    finalScore[name] += score
    
maxScore = max(finalScore.values())
runningScore = defaultdict(int)
for name, score in rounds:
    runningScore[name] += score
    if runningScore[name] >= maxScore and finalScore[name] == maxScore:
        print(name)
        break