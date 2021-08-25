import json
from pathlib import Path

vocab = {
        'battery': ["drain", "swell"], 
        'internet': [],
        'bluetooth': ['bluetooth'],
        'usb/type-c': ['type-c', 'usb'],
        'device connection': ['tv cast'],
        'software/system update':['after upgra', 'after upda', 'after the up'],
        'screen': [],
        'virtual assistant': [],
        'headphone': [],
        'audio/voice': [],
        'app': [],
        'notification': ['notification','do not disturb', 'alarm', 'ringtone'],
        'camera/multimedia': ['lense', 'night sight', 'astrophotography'],
        'sim/esim': ['esim', 'sim'],
        'communication': ['voicemail', 'screen call'],
        'account': [],
        'security': ['screen lock', 'fingerprint', 'face recognition'],
        'boot': [],
        'storage': [],
        'backup': ['restore', 'backup'],
        'setup': [],
        'gps': ['gps'],
        'user interface':['gesture', 'swipe'],
        'feature request':[],
        'appearance': [],
        'customer service': ['warranti', 'repair', 'support'],
        'other': [],
        'useless': []
        }

data_path = Path('../../raw_data/data35000.json')

if __name__ == '__main__':
    with open(data_path, 'r') as f:
        data = json.load(f)
    #print(data)
    multi_data = {}
    count = 0
    multilabel_count = 0
    '''
    for key, value in data.items():
        newdata = {'data': value, 'label': []}
        content = value['title'] + " " + value['content']
        content = content.lower()
        for label_name, label_keywords in vocab.items():
            for keyword in label_keywords:
                if keyword in content:
                    newdata['label'].append(label_name)
                    break
        multi_data[key] = newdata
        if len(newdata['label']) > 0:
            count += 1
        if len(newdata['label']) > 1:
            multilabel_count += 1
    print("# data {0}, # label data {1}, # multilabel data {2}".format(len(multi_data), count, multilabel_count))
    with open(Path('./labeldata.json'), 'w') as f:
        json.dump(multi_data, f, indent=2)
    '''
    multi_data = {}
    count = 0
    multilabel_coumt = 0
    with open("vocab.json",'r') as f:
        pachi_vocab = json.load(f)
    for key, value in data.items():
    
        newdata = {'data':value, 'label':[]}
    
        content = value['title'] + " " + value['content']
        content = content.lower()
        for label_name, label_keywords in pachi_vocab.items():
            feq_counter = 0
            for keyword in label_keywords:
                if keyword in content:
                    feq_counter += 1
            if feq_counter >= 5:
                if label_name == '0':
                    newdata['label'].append('notification')
                if label_name == '1':
                    newdata['label'].append('internet')
                if label_name == '2':
                    newdata['label'].append('audio/voice')
                    if 'youtub' in content:
                        newdata['label'].append('app')
                if label_name == '3':
                    newdata['label'].append('security')
                if label_name == '4':
                    newdata['label'].append('account')
                    if 'gmail' in content:
                        newdata['label'].append('app')
                if label_name == '5':
                    newdata['label'].append('audio/voice')
                if label_name == '6':
                    pass
                if label_name == '7':
                    newdata['label'].append('app')
                if label_name == '8':
                    pass
                if label_name == '9':
                    if 'chrome' in content:
                        newdata['label'].append('app')
                if label_name == '10':
                    if 'facebook' in content:
                        newdata['label'].append('app')
                if label_name == '11':
                    newdata['label'].append('virtual assistant')
                if label_name == '12':
                    pass
                if label_name == '13':
                    if 'camera' in content:
                        newdata['label'].append('camera/multimedia')
                    if 'app' in content:
                        newdata['label'].append('app')
                if label_name == '14':
                    newdata['label'].append('sim/esim')
                if label_name == '15':
                    newdata['label'].append('camera/multimedia')
                if label_name == '16':
                    newdata['label'].append('screen')
                if label_name == '17':
                    newdata['label'].append('battery')
                if label_name == '18':
                    pass
                if label_name == '19':
                    newdata['label'].append('communication')
                if label_name == '20':
                    newdata['label'].append('customer service')
                if label_name == '21':
                    newdata['label'].append('internet')
                if label_name == '22':
                    pass
                if label_name == '23':
                    newdata['label'].append('bluetooth')
                    if 'headphon' in content:
                        newdata['label'].append('headphone')
                if label_name == '24':
                    pass
                if label_name == '25':
                    pass
                if label_name == '26':
                    pass
                if label_name == '27':
                    newdata['label'].append('gps')
                if label_name == '28':
                    pass
                if label_name == '29':
                    newdata['label'].append('storage')
                if label_name == '30':
                    newdata['label'].append('software/system update')
                if label_name == '31':
                    newdata['label'].append('battery')
                if label_name == '32':
                    newdata['label'].append('screen')
                if label_name == '33':
                    pass
                if label_name == '34':
                    newdata['label'].append('user interface')
                if label_name == '35':
                    newdata['label'].append('screen')
                if label_name == '36':
                    newdata['label'].append('backup')
                if label_name == '37':
                    newdata['label'].append('storage')
                if label_name == '38':
                    newdata['label'].append('communication')
                if label_name == '39':
                    newdata['label'].append('other')
                if label_name == '40':
                    pass
                if label_name == '41':
                    newdata['label'].append('communication')
                if label_name == '42':
                    newdata['label'].append('audio')
                if label_name == '43':
                    pass
                if label_name == '44':
                    pass
                if label_name == '45':
                    pass
                if label_name == '46':
                    newdata['label'].append('customer service')
                if label_name == '47':
                    newdata['label'].append('battery')
                if label_name == '48':
                    newdata['label'].append('customer service')
                    if "screen" in content:
                        newdata['label'].append('screen')
                if label_name == '49':
                    newdata['label'].append('software/system update')

        for label_name, label_keywords in vocab.items():
           for keyword in label_keywords:
               if keyword in content:
                   newdata['label'].append(label_name)
                   break
        category = value['category'].lower()
        if 'google assistant and voice actions' in category:
            newdata['label'].append('virtual assistant')
        if 'homescreen and launcher' in category:
            newdata['label'].append('user interface')
        if 'camera' in category:
            newdata['label'].append('camera/multimedia')
        if 'setting up and personalizing your' in category:
            newdata['label'].append('setup')
        if 'contacts, calls, voicemail' in category:
            newdata['label'].append('communication')
        if 'battery and power' in category:
            newdata['label'].append('battery')
        _ = set(newdata['label'])
        newdata['label'] = list(_)
        multi_data[key] = newdata
        if len(newdata['label']) > 0:
            count += 1
        if len(newdata['label']) > 1:
            multilabel_count += 1
    print("# data {0}, # label data {1}, # multilabel data {2}".format(len(multi_data), count, multilabel_count))
    with open(Path('./labeldata.json'), 'w') as f:
        json.dump(multi_data, f, indent=2)

