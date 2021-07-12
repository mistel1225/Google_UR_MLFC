import json
import logging
import os
from pathlib import Path
import numpy as np

H = "-h"
PC = "-pc"
PL = "-pl"
LD = "-ld"
NL = "-nl"
E = "-e"
NS = "-ns"
COMMAND_DICT = {H:"list all command", PC:"print context", PL:"print available label", LD:"label the data", NL:"append new label", NS:"sample new data immediately", E:"exit the program"}

def read_json(path):
    with open(str(path), 'r') as f:
        data = json.load(f)
    return data
#TODO need sync module
def save_json(data, path):
    logging.info("save the data {0}...".format(path))
    with open(str(path), 'w') as f:
        json.dump(data, f, indent=2)
def show_command():
    for key, value in COMMAND_DICT.items():
        print("{0} {1}".format(key, value))
def print_label(label_list):
    for label, des in label_list.items():
        print("{0}: {1}".format(label, des))


def create_label(label_list, label, description):
    if label not in label_list.keys():
        label_list[label] = description
    else:
        print("the label {0} has already existed the list.".format(label))
    return label_list

def print_context(sample_data):
    print("---------title---------\n{0}\n---------post_time---------\n{1}\n---------content---------\n{2}".format(sample_data['title'], sample_data['post_time'], sample_data['content']))
    print("---------url-----------\n{0}".format(sample_data['url']))
def label_data(labeled_data, sample_data, sample_index, label_list, label, answer_span, annotated_index):
    if label not in label_list.keys():
        print("error: this label is not exists in label_list currently")
        return labeled_data
    if sample_index not in labeled_data.keys():
        labeled_data[sample_index] = {"data":sample_data, "label":{label:answer_span}}
    else:
        labeled_data[sample_index]["label"][label] = answer_span
    annotated_index[sample_index] = {"label":1, "verify":0}
    return labeled_data, annotated_index

def label_new_data(sample_num, data_path, index_path, label_path, output_path):
    data = read_json(data_path)
    show_command()    
    data_length = len(data)
    print(data_length)
    for i in range(sample_num):
        print("({0}/{1})".format(i+1, sample_num))
        #TODO need sync module
        annotated_index = read_json(index_path)
        label_list = read_json(label_path)
        labeled_data = read_json(output_path)
        #random sample the data
        while(1):
            sample_index = np.random.randint(data_length)
            if sample_index in annotated_index.keys():
                if annotated_index[sample_index]['label'] == 0:
                    break
                else:
                    break
            else:
                break
        sample_data = data[str(sample_index)]
        print_context(sample_data)
        while(1):
            command = str(input("type command:"))
            if command not in COMMAND_DICT.keys():
                print("command not found, try again.")
                continue
            if command == H:
                show_command()
            elif command == PC:
                print_context(sample_data)
                continue
            elif command == PL:
                print_label(label_list)
                continue
            elif command == NL:
                new_label = str(input("label:"))
                label_discription = str(input("label discription:"))
                label_list = create_label(label_list, new_label, label_discription)
                save_json(label_list, label_path)
            elif command == NS:
                break
            elif command == E:
                save_json(label_list, label_path)
                save_json(annotated_index, index_path)
                save_json(labeled_data, output_path)
                logging.info('exit')
                exit(0)
            elif command == LD:
                sample_data['content'].replace("$", "")
                print_label(label_list)
                print("one label per round.")
                label = input("label:")
                answer_span = input("answer(use \"$\" as split symbol):")
                labeled_data, annotated_index = label_data(labeled_data, sample_data, sample_index,label_list, label, answer_span, annotated_index)
                save_json(labeled_data, output_path)
                save_json(annotated_index, index_path)
