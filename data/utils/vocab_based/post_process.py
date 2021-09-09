import json
with open('labeldata.json', 'r') as f:
    data = json.load(f)


#with open('data_label.json', 'r') as f:
#    label = json.load(f)

battery_dict = {}
bluetooth_dict = {}
camera_dict = {}
gps_dict = {}
communication_dict = {}
for k, d in data.items():
    if len(d["label"]) > 1:
        continue
    elif 'battery' in d["label"]:
        d.pop('label')
        battery_dict[len(battery_dict)] = d['data']
    elif 'bluetooth' in d["label"]:
        d.pop('label')
        bluetooth_dict[len(bluetooth_dict)] = d['data']
    elif 'camera' in d['label']:
        d.pop('label')
        camera_dict[len(camera_dict)] = d['data']
    elif 'gps' in d['label']:
        d.pop('label')
        gps_dict[len(gps_dict)] = d['data']
    elif 'communication' in d['label']:
        d.pop('label')
        communication_dict[len(communication_dict)] = d['data']
dict_list = {'battery_data': battery_dict, 'bluetooth_data': bluetooth_dict, 'camera_data': camera_dict, 'gps_data':gps_dict, 'communication_data': communication_dict}

for dic_name, dic in dict_list.items():
    with open(dic_name+'.json', 'w') as f:
        json.dump(dic, f, indent=2)


