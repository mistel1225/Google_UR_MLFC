import json
from pathlib import Path
import sys
sys.path.append("../../../baseline_model/PLDA")
import plda_inference
from plda_inference import inference
import tomotopy as tp
from tqdm import tqdm
vocab = {
        'battery': ["drain", "swell"], 
        'internet': [],
        'bluetooth': ['bluetooth'],
        'usb/type-c': ['type-c', 'usb'],
        'camera': ['lense', 'night sight', 'astrophotography'],
        'sim/esim': ['esim', 'sim'],
        'screen': [],
        'appearance': [],
        'storage': [],
        'speaker': [], 
        'headphone': [],

        'software/system update':['after upgra', 'after upda', 'after the up', 'updat', 'upgrad'],
        'google app': [],
        'third party app': [],
        'account': [],
        'boot': [],
        'backup': ['restore', 'backup'],
        'virtual assistance': [],

        'audio/voice': [],
        'notification': ['do not disturb', 'alarm', 'ringtone'],
        'communication': ['voicemail', 'screen call'],
        'multimedia': [],
        'security': ['screen lock', 'fingerprint', 'face recognition'],
        'device connection': ['cast'],
        'gps': ['gps'],
        'system service':['gesture', 'swipe', 'launcher', 'keyboard'],
        
        'feature request and suggestion':[],
        'customer service': ['warrant', 'repair', 'support'],
        'setup':[], 
        
        'stability':[],

        'other': [],
        'useless': []
        }
vocab_index = {i:label for i, label in enumerate(vocab.keys())}
vocab_index_reverse = {label:i for i, label in enumerate(vocab_index.values())}

path_dict = {'g':Path('../../raw_data/data35000.json'), 's_uk':Path('../../raw_data/samsungdatauk.json'), 's_us':Path('../../raw_data/samsungdataus.json')}

if __name__ == '__main__':
    #print(data)
    multi_data = {}
    count = 0 # labeled data count
    multilabel_count = 0 # multi labeled data count
    data_count = 0 # num of data
    multi_data = {}
    with open("vocab.json",'r') as f:
        pachi_vocab = json.load(f)
    lda_model = tp.PLDAModel().load('../../../baseline_model/PLDA/PLDA_for_1000_labeled_data.model')
  
    for data_name, data_path in path_dict.items():
        with open(data_path, 'r') as f:
            data = json.load(f)
        for key, value in tqdm(data.items()):
            newdata = {'data':value, 'label':[]}
            content = value['title'] + " " + value['content']
            content = content.lower()
            for label_name, label_keywords in pachi_vocab.items():
                feq_counter = 0
                for keyword in label_keywords:
                    if keyword in content:
                        feq_counter += 1
                threshold = 4
                if data_name == 'g':
                    threshold = 5
                if feq_counter >= threshold:
                    if label_name == '0':
                        newdata['label'].append(vocab_index[vocab_index_reverse['notification']])
                    if label_name == '1':
                        newdata['label'].append(vocab_index[vocab_index_reverse['internet']])
                    if label_name == '2':
                        newdata['label'].append(vocab_index[vocab_index_reverse['audio/voice']])
                        if 'youtub' in content:
                            newdata['label'].append(vocab_index[vocab_index_reverse['google app']])
                    if label_name == '3':
                        newdata['label'].append(vocab_index[vocab_index_reverse['security']])
                    if label_name == '4':
                        newdata['label'].append(vocab_index[vocab_index_reverse['account']])
                        if 'gmail' in content:
                            newdata['label'].append(vocab_index[vocab_index_reverse['google app']])
                    if label_name == '5':
                        newdata['label'].append(vocab_index[vocab_index_reverse['audio/voice']])
                    if label_name == '6':
                        pass
                    if label_name == '7':
                        newdata['label'].append(vocab_index[vocab_index_reverse['audio/voice']])
                    if label_name == '8':
                        pass
                    if label_name == '9':
                        if 'chrome' in content:
                            newdata['label'].append(vocab_index[vocab_index_reverse['google app']])
                    if label_name == '10':
                        if 'facebook' in content:
                            newdata['label'].append(vocab_index[vocab_index_reverse['third party app']])
                    if label_name == '11':
                        newdata['label'].append(vocab_index[vocab_index_reverse['google app']])
                    if label_name == '12':
                        pass
                    if label_name == '13':
                        if 'camera' in content:
                            newdata['label'].append(vocab_index[vocab_index_reverse['camera']])
                    if label_name == '14':
                        newdata['label'].append(vocab_index[vocab_index_reverse['sim/esim']])
                    if label_name == '15':
                        newdata['label'].append(vocab_index[vocab_index_reverse['camera']])
                    if label_name == '16':
                        newdata['label'].append(vocab_index[vocab_index_reverse['screen']])
                    if label_name == '17':
                        newdata['label'].append(vocab_index[vocab_index_reverse['battery']])
                    if label_name == '18':
                        pass
                    if label_name == '19':
                        newdata['label'].append(vocab_index[vocab_index_reverse['communication']])
                    if label_name == '20':
                        newdata['label'].append(vocab_index[vocab_index_reverse['customer service']])
                    if label_name == '21':
                        newdata['label'].append(vocab_index[vocab_index_reverse['internet']])
                    if label_name == '22':
                        pass
                    if label_name == '23':
                        newdata['label'].append(vocab_index[vocab_index_reverse['bluetooth']])
                        if 'headphon' in content:
                            newdata['label'].append(vocab_index[vocab_index_reverse['headphone']])
                    if label_name == '24':
                        pass
                    if label_name == '25':
                        pass
                    if label_name == '26':
                        pass
                    if label_name == '27':
                        newdata['label'].append(vocab_index[vocab_index_reverse['gps']])
                    if label_name == '28':
                        pass
                    if label_name == '29':
                        newdata['label'].append(vocab_index[vocab_index_reverse['storage']])
                    if label_name == '30':
                        newdata['label'].append(vocab_index[vocab_index_reverse['software/system update']])
                    if label_name == '31':
                        newdata['label'].append(vocab_index[vocab_index_reverse['battery']])
                    if label_name == '32':
                        newdata['label'].append(vocab_index[vocab_index_reverse['screen']])
                    if label_name == '33':
                        pass
                    if label_name == '34':
                        newdata['label'].append(vocab_index[vocab_index_reverse['system service']])
                    if label_name == '35':
                        newdata['label'].append(vocab_index[vocab_index_reverse['screen']])
                    if label_name == '36':
                        newdata['label'].append(vocab_index[vocab_index_reverse['backup']])
                    if label_name == '37':
                        newdata['label'].append(vocab_index[vocab_index_reverse['storage']])
                    if label_name == '38':
                        newdata['label'].append(vocab_index[vocab_index_reverse['communication']])
                    if label_name == '39':
                        pass
                    if label_name == '40':
                        pass
                    if label_name == '41':
                        newdata['label'].append(vocab_index[vocab_index_reverse['communication']])
                    if label_name == '42':
                        newdata['label'].append(vocab_index[vocab_index_reverse['audio/voice']])
                    if label_name == '43':
                        pass
                    if label_name == '44':
                        pass
                    if label_name == '45':
                        pass
                    if label_name == '46':
                        newdata['label'].append(vocab_index[vocab_index_reverse['customer service']])
                    if label_name == '47':
                        newdata['label'].append(vocab_index[vocab_index_reverse['battery']])
                    if label_name == '48':
                        newdata['label'].append(vocab_index[vocab_index_reverse['customer service']])
                        if "screen" in content:
                            newdata['label'].append(vocab_index[vocab_index_reverse['screen']])
                    if label_name == '49':
                        newdata['label'].append(vocab_index[vocab_index_reverse['software/system update']])
    
    
            for label_name, label_keywords in vocab.items():
               for keyword in label_keywords:
                   if keyword in content:
                       newdata['label'].append(vocab_index[vocab_index_reverse[label_name]])
                       break
            if data_name == 'g':
                category = value['category'].lower()
                if 'google assistant and voice actions' in category:
                    newdata['label'].append(vocab_index[vocab_index_reverse['google app']])
                if 'homescreen and launcher' in category:
                    newdata['label'].append(vocab_index[vocab_index_reverse['system service']])
                if 'camera' in category:
                    newdata['label'].append(vocab_index[vocab_index_reverse['camera']])
                if 'setting up and personalizing your' in category:
                    newdata['label'].append('setup')
                if 'contacts, calls, voicemail' in category:
                    newdata['label'].append(vocab_index[vocab_index_reverse['communication']])
                if 'battery and power' in category:
                    newdata['label'].append(vocab_index[vocab_index_reverse['battery']])
            
            result, jaccard_score = inference(mdl=lda_model, title=value['title'], content=value['content'], print_detail=False, threshold=0.45)
            for l in result:
                if l.lower() not in vocab_index.values():
                    print("{} not in label list".format(l.lower()))
                newdata['label'].append(l.lower())
            _ = set(newdata['label'])
            newdata['label'] = list(_)
            multi_data[data_count] = newdata
            if len(newdata['label']) > 0:
                count += 1
            if len(newdata['label']) > 1:
                multilabel_count += 1
            data_count += 1
            


    print("# data {0}, # label data {1}, # multilabel data {2}".format(len(multi_data), count, multilabel_count))
    with open(Path('./labeldata.json'), 'w') as f:
        json.dump(multi_data, f, indent=2)

