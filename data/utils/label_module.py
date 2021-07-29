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
COMMAND_DICT = {H:"list all command", PC:"print context", PL:"print available label", LD:"label the data", NL:"append new label", NS:"sample new data immediately", E:"exit the program"}

def show_command():
    for key, value in COMMAND_DICT.items():
        print("{0} {1}".format(key, value))
def print_label(label_list):
    for label, des in label_list.items():
        print("{0}: {1}".format(label, des))



def print_context(sample_data):
    content = textwrap.fill(sample_data['content'], width=80)
    print("---------title---------\n{0}\n---------post_time---------\n{1}\n---------content---------\n{2}".format(sample_data['title'], sample_data['post_time'], content))
    print("---------url-----------\n{0}".format(sample_data['url']))

def label_new_data(sample_num, data_path, index_path, label_path, output_path):
    data = read_json(data_path)
    show_command()    
    data_length = len(data)
    for i in range(sample_num):
        print("({0}/{1})".format(i+1, sample_num))
        #TODO need sync module
        annotated_index = read_json(index_path)
        label_list = read_json(label_path)
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
                label_list = read_json(label_path)
                print_label(label_list)
                continue
            elif command == NL:
                new_label = str(input("label:"))
                label_discription = str(input("label discription:"))
                label_list = create_label(label_path, new_label, label_discription)
            elif command == NS:
                break
            elif command == E:
                logging.info('exit')
                exit(0)
            elif command == LD:
                sample_data['content'].replace("$", "")
                print_label(label_list)
                print("one label per round.")
                #annotation
                label = input("label:")
                answer_span = input("answer(use \"$\" as split symbol):")
                labeled_data, annotated_index = label_data(sample_data, sample_index, label, answer_span, index_path, label_path, output_path)
