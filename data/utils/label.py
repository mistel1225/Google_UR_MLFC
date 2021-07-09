import argparse
import json
from pathlib import Path
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', help=
            'sample {num} data from data/raw_data/data35000.json(for new data) or data/multi_label_data(for verify data)', 
            type=int, default=50)
    parser.add_argument('-m', '--mode', help=
    'new: sample new data. verify:sample the data that is already being labeled',
            type=str, default='new')
    parser.add_argument('--dp', '--data_path', help='../raw_data/{data with no label}.json, 
            ../multi_label_data/{data already being labeled}.json', 
            type=Path, default='../raw_data/data35000.json')
    parser.add_argument('--op', '--output_path', help=
            'for experiment usage: ../multi_label_data/{name of whatever you want}.json, 
            for labeling usage: ../multi_label_data/data35000label.json', 
            type=Path, default='../multi_label_data/data35000label.json')
    parser.add_argument('--ip', '--index_path', help=
            'path to store the index of the data that has been annotated.', 
             type=Path, default='./annotated_id')
    parser.add_argument('--lp', '--label_path.json', help=
            'path to store the label.'
            type=Path, default='./data_label.json')
    args = parser.parse_args()
    return args

def read_json(path):
    with open(str(path), 'r') as f:
        data = json.loads(f)
    logging.debug('{0} is successfully being load'.format(path))
    return data
def init_file(path):
    logging.debug('{0} didn\'t exists, create new file.'.format(path))
    open(str(path), 'x')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    if args.n <= 0:
        logging.debug('{0} <= 0, program shut down.'.format(args.n))
        exit(-1)
    if !args.dp.exists():
        logging.debug('{0} didn\'t exists.')
        exit(-1)
    else:
        data = read_json(args.dp)
    if !args.op.exists():
        init_file(args.op)
    if !args.ip.exists():
        init_file(args.ip)
    if !args.lp.exists():
        init_file(args.lp)
    main(args)
    


    main(args)

