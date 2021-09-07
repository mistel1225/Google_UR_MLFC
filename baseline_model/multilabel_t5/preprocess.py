import json
def process_train():
    with open('labeldata.json', 'r') as f:
        data = json.load(f)
    idx = 0
    length = 0
    multi_count = 0
    new_data = {}
    for k, d in data.items():
        if len(d['label']) > 0:
            new_data[idx] = d
            idx+=1
        if len(d['label']) > 1:
            multi_count+=1
        length+=len(d['data']['title']+d['data']['content'])
    length/=len(data)
    with open('train.json', 'w') as f:
        json.dump(new_data, f, indent=2)
    print("# data={0}, # multi-label data={1}, avg length={2}".format(idx, multi_count, length))
def process_val():
    with open('labeldata1000.json', 'r') as f:
        data = json.load(f)
    idx = 0
    new_data = {}
    for k, d in data.items():
        if len(d['label']) > 0:
            new_data[idx] = d
            idx+=1
    with open('val.json', 'w') as f:
        json.dump(new_data, f, indent=2)
def process_nolabel():
    with open('labeldata.json', 'r') as f:
        data = json.load(f)
    idx = 0
    length = 0
    multi_count = 0
    new_data = {}
    for k, d in data.items():
        if len(d['label']) == 0:
            new_data[idx] = d
            idx+=1
        #length+=len(d['data']['title']+d['data']['content'])
    #length/=len(data)
    with open('nolabeldata.json', 'w') as f:
        json.dump(new_data, f, indent=2)
   
