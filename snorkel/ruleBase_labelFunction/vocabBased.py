#from snorkel.labeling import labeling_function

ABSTAIN = -1
Battery = 0
Camera = 1
Network = 2
Call = 3
Assistant = 4
Homescreen = 5
Setting = 6

vocab = {
    0 : ["drain", "swell", "battery"],
    1 : ["lense", "night sight", "astrophotography", "camera"],
    2 : ["wifi", "wi-fi", "sim card", "esim", "4g", "lte", "5g"],
    3 : ["voicemail", "screen call", "calls"],
    4 : ["google assist", "virtual assist", "ok google", "assistant"],
    5 : ["homescreen", "launcher"],
    6 : ["setup", "how to"]
}

#@labeling_function()
def vocab_based(d):
    text = d['title'] + ' ' + d['content']
    text = text.lower()
    cnt = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        vocab_list = vocab[i]
        for v in vocab_list:
            if v in text:
                cnt[i] = 1
                break
    if sum(cnt) > 1 or sum(cnt) == 0:
        return ABSTAIN
    else:
        for i in range(7):
            if cnt[i] == 1:
                return i


import json
with open('rawdata.json', 'r') as f:
    data = json.load(f)
cnt = {}
for d in data.values():
    res = vocab_based(d)
    if res not in cnt.keys():
        cnt[res] = 1
    else:
        cnt[res] += 1
print(cnt)



