import json

if __name__ == '__main__':
    with open('data35000.json', 'r') as f:
        data = json.load(f)
    new_data = {}
    idx=0
    for item in data['data']:
        new_data[idx] = item
        idx+=1
    with open('data35000.json', 'w') as f:
        json.dump(new_data, f, indent=2)
