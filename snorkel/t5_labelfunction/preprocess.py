import json
from sklearn.model_selection import train_test_split
with open('data35000.json', 'r') as f:
    data_file = json.load(f)
data = []
count = [0, 0, 0, 0, 0, 0, 0]
idx = 0
null_idx = 0
for _ in data_file.values():
    label = -1
    if 'Battery and Power' in _['category']:
        label = 0
        count[0]+=1
    elif 'Camera' in _['category']:
        label = 1
        count[1]+=1
    elif 'Connectivity, Network, Bluetooth' in _['category']:
        label = 2
        count[2]+=1
    elif 'Contacts, Calls, Voicemail' in _['category']:
        label = 3
        count[3]+=1
    elif 'Google Assistant and Voice Actions' in _['category']:
        label = 4
        count[4]+=1
    elif 'Homescreen and Launcher' in _['category']:
        label = 5
        count[5]+=1
    elif 'Setting up and Personalizing your Device' in _['category']:
        label = 6
        count[6]+=1
    if label != -1:
        data.append({'idx': idx, 'title':_['title'], 'content':_['content'], 'label':label})
        idx+=1
train, test = train_test_split(data, test_size=0.2, shuffle=True, random_state=42)
label_dict = {
        0:'Battery and Power',
        1:'Camera',
        2:'Connectivity, Network, Bluetooth',
        3:'Contacts, Calls, Voicemail',
        4:'Google Assistant and Voice Actions',
        5:'Homescreen and Launcher',
        6:'Setting up and Personalizing your Device'
        }
print(count)
with open('train.json', 'w') as f:
    json.dump(train, f, indent=2)
with open('dev.json', 'w') as f:
    json.dump(test, f, indent=2)
with open('label_dict.json', 'w') as f:
    json.dump(label_dict, f, indent=2)
