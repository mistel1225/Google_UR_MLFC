import json
import logging
from pathlib import Path
lock_path = "./"
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
            if int(f.read()) == 0:
                f.seek(0)
                f.write("1")
                break
def restore_lock():
    logging.info("reset the file lock...")
    with open(lock_path+'data.lock', 'r+') as f:
        f.seek(0)
        f.write("0")

def label_data(sample_data, sample_index, label, answer_span, index_path, label_path, output_path):
    #get the lock
    get_lock()
    #critical section
    #update the data in memory
    labeled_data = read_json(output_path)
    annotated_index = read_json(index_path)
    label_list = read_json(label_path)
    #assign the label to the data
    if label not in label_list.keys():
        print("error: this label doesn't exist in label_list currently.")
        restore_lock()
        return labeled_data, annotated_index
    if sample_index not in labeled_data.keys():
        labeled_data[sample_index] = {"data":sample_data, "label":{label:answer_span}}
    else:
        labeled_data[sample_index]["label"][label] = answer_span
    annotated_index[sample_index] = {"label":1, "verify":0}
    #update the data in file system
    save_json(labeled_data, output_path)
    save_json(annotated_index, index_path)
    #end of the critical section, restore the lock
    restore_lock()
    return labeled_data, annotated_index
def create_label(label_path, label, discription):
    get_lock()
    label_list = read_json(label_path)
    if label not in label_list.keys():
        label_list[label] = discription
    else:
        print("the label {0} has already existed in the list".format(label))
    save_json(label_list ,label_path)
    restore_lock()
    return label_list
    
