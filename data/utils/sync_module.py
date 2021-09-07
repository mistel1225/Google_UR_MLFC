import json
import logging
from pathlib import Path
from time import sleep
lock_path = "../remote_mount_data/"
def read_json(path):
    with open(str(path), 'r') as f:
        data = json.load(f)
    return data
def save_json(data, path):
    logging.info("save the data {0}...".format(path))
    with open(str(path), 'w') as f:
        json.dump(data, f, indent=2)

def get_lock():
    if not Path(lock_path+'data.lock').exists():
        logging.info('{0} didn\'t existst, create new lock file...'.format(lock_path+'data.lock'))
        with open(lock_path+'data.lock', 'x') as f:
            f.write("0")
    logging.info("get the file lock...")
    while(1):
        with open(lock_path+'data.lock', 'r+') as f:
            try:
                if int(f.read()) == 0:
                    f.seek(0)
                    f.write("1")
                    break
            except:
                sleep(1)
def restore_lock():
    logging.info("reset the file lock...")
    with open(lock_path+'data.lock', 'r+') as f:
        f.seek(0)
        f.write("0")
def read_label_dict(label_path):
    label_dict = read_json(label_path)
    idx = 0
    label_list = []
    for sub_label_list in label_dict.values():
        for l in sub_label_list:
            label_list.append(l)
    label_list = sorted(label_list)
    idx_label_dict = {idx: l for idx, l in enumerate(label_list)}
    return idx_label_dict
def label_data(sample_data, sample_index, label: str, index_path, label_path, output_path, worker_name:str):
    #get the lock
    get_lock()
    #critical section
    #update memory's data
    labeled_data = read_json(output_path)
    annotated_index = read_json(index_path)
    idx_label_dict = read_label_dict(label_path)
    #assign the label to the data
    if label not in idx_label_dict.values():
        print("error: this label doesn't exist in label_list currently.")
        restore_lock()
        return labeled_data, annotated_index
    if str(sample_index) not in labeled_data.keys():
        labeled_data[str(sample_index)] = {"data":sample_data, "label":[label], "worker_name": [worker_name]}
        annotated_index[str(sample_index)] = {"label":1, "verify":0}
    else:
        labeled_data[str(sample_index)]["label"].append(label)
        labeled_data[str(sample_index)]["worker_name"].append(worker_name)
        labeled_data[str(sample_index)]["worker_name"] = list(set(labeled_data[str(sample_index)]["worker_name"]))
    #update the data in file system
    save_json(labeled_data, output_path)
    save_json(annotated_index, index_path)
    #end of the critical section, restore the lock
    restore_lock()
    return labeled_data, annotated_index
def create_label(label_path, label, discription):
    print("WARNNING: this version doesn't support create new label.")
    get_lock()
    label_list = read_json(label_path)
    if label not in label_list.keys():
        label_list[label] = discription
    else:
        print("the label {0} has already existed in the list".format(label))
    save_json(label_list ,label_path)
    restore_lock()
    return label_list
    
