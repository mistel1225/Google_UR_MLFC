import json

cnt = 0
data = {}
while(1):
    s = input()
    if s == '-e':
        break
    data[cnt] = s.split(" ")
    cnt+=1

with open('vocab.json', 'w') as f:
    json.dump(data, f, indent=2)

