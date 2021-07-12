import argparse
import json
from pathlib import Path
import os
import logging
from label_module import label_new_data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', help=
            'sample {num} data from data/raw_data/data35000.json(for new data) or data/multi_label_data(for verify data)', 
            type=int, default=50)
    parser.add_argument('-m', '--mode', help=
    'new: sample new data. verify:sample the data that is already being labeled',
            type=str, default='new')
    parser.add_argument('-dp', '--data_path', help=
            '../raw_data/{data with no label}.json, ../multi_label_data/{data already being labeled}.json', 
            type=Path, default='../raw_data/data35000.json')
    parser.add_argument('-op', '--output_path', help=
    'for experiment usage: ../multi_label_data/{name of whatever you want}.json, for labeling usage: ../multi_label_data/data35000label.json', 
            type=Path, default='../multi_label_data/data35000label.json')
    parser.add_argument('-ip', '--index_path', help=
            'path to store the index of the data that has been annotated.', 
             type=Path, default='./annotated_id.json')
    parser.add_argument('-lp', '--label_path', help=
            'path to store the label.',
            type=Path, default='./data_label.json')
    args = parser.parse_args()
    return args

def read_json(path):
    with open(str(path), 'r') as f:
        data = json.load(f)
    logging.info('{0} is successfully being load'.format(path))
    return data
def init_file(path):
    if not path.exists():
        logging.info('{0} didn\'t exists, create new file...'.format(path))
        with open(str(path), 'x') as f:
            json.dump({}, f)
    else:
        logging.info('{0} already exists, continue to run the program...'.format(path))
mode = ['new', 'verify']

def main(args):
    
    if args.mode == 'new':        
        label_data = label_new_data(args.num, args.data_path, args.index_path, args.label_path, args.output_path)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    if args.num <= 0:
        logging.error('{0} <= 0, program shut down.'.format(args.num))
        exit(-1)
    if not args.data_path.exists():
        logging.error('{0} didn\'t exists.')
        exit(-1)
    else:
        data = read_json(args.data_path)
    init_file(args.output_path)
    init_file(args.index_path)
    init_file(args.label_path)
    if args.mode not in mode:
        logging.error('{} is not in default mode [\'new\', \'verify\']')
        exit(-1)
    if args.mode == 'verify' and str(args.data_path) == '../raw_data/data35000.json':
        logging.error('{0} verify mode fail, the data_path should under ../data/multi_label_data')
    main(args)
    



