import json
import logging
import os
from pathlib import Path
from sync_module import label_data, create_label, read_json
import numpy as np
import textwrap

H = "-h"
PC = "-pc"
PL = "-pl"
LD = "-ld"
NL = "-nl"
E = "-e"
NS = "-ns"
S = '-s'
COMMAND_DICT = {H:"list all command", PC:"print context", PL:"print available label", LD:"label the data", NL:"append new label", NS:"sample new data immediately", E:"exit the program", S:'show the current sample\'s label'}



def show_command():
    for key, value in COMMAND_DICT.items():
        print("{0} {1}".format(key, value))


def print_label(idx_label_dic):
    s=''
    for i, (idx, label) in enumerate(idx_label_dic.items()):
        s += '{:>2d}: {:<30}'.format(idx,str(label.title()))
        if (i+1)%4 ==0:
            print(s)
            s=''
    print(s)
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

def print_context(sample_data):
    content = textwrap.fill(sample_data['content'], width=80)
    print("---------title---------\n{0}\n---------content---------\n{1}".format(sample_data['title'], content))
    print("---------url-----------\n{0}".format(sample_data['url']))

def label_new_data(sample_num, data_path, index_path, label_path, output_path, worker_name:str):
    data = read_json(data_path)
    show_command()    
    data_length = len(data)
    for i in range(sample_num):
        print("({0}/{1})".format(i+1, sample_num))
        annotated_index = read_json(index_path)
        #label_dict = read_json(label_path)
        #idx_label_dic = {i:label for i, label in zip(range(len(label_list)), label_list.keys())}
        idx_label_dic = read_label_dict(label_path)
        labeled_data = read_json(output_path)
        #random sample the data
        while(1):
            sample_index = np.random.randint(data_length)
            if str(sample_index) not in annotated_index.keys():
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
                #label_dict = read_json(label_path)
                #idx_label_dic = {i:label for i, label in zip(range(len(label_list)), label_list.keys())}       
                idx_label_dic = read_label_dict(label_path)
                print_label(idx_label_dic)
                continue
            elif command == NL:
                '''
                new_label = str(input("label:"))
                label_discription = str(input("label discription:"))
                label_list = create_label(label_path, new_label, label_discription)
                '''
                print("Doesn't support this feature now. Please discuss it with others")
            elif command == NS:
                break
            elif command == E:
                logging.info('exit')
                exit(0)
            elif command == LD:
                sample_data['content'].replace("$", "")
                #label_dict = read_json(label_path)
                idx_label_dic = read_label_dict(label_path)
                #idx_label_dic = {i:label for i, label in zip(range(len(label_list)), label_list.keys())}
                print_label(idx_label_dic)
                print("one label per round.")
                #annotation
                label = input("label:")
                try:
                    idx_label_dic[int(label)]
                except:
                    print('idx not exists, try again')
                    continue
                labeled_data, annotated_index = label_data(sample_data, sample_index, idx_label_dic[int(label)], index_path, label_path, output_path, worker_name)
            elif command == S:
                labeled_data = read_json(output_path)
                try:
                    _ = labeled_data[str(sample_index)]
                    s = ''
                    for i, label in enumerate(_["label"]):
                        s+="{:<30}".format(label)
                        if (i+1)%4==0:
                            print(s)
                            s=''
                    print(s)
                except:
                    print("didn't label yet")

