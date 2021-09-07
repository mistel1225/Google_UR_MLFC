import json
from pathlib import Path
path_dict = {"g": Path("./data35000.json"), "s_uk": Path("./samsungdatauk.json"), "s_us": Path("./samsungdataus.json")}


def combine_raw_data():
    idx = 0
    data = {}
    for p in path_dict.values():
        with open(p, 'r') as f:
            _ = json.load(f)
        for k, d in _.items():
            if "category" in d.keys():
                d["tag_list"] = d["category"].split(',')
                d.pop("category")
            data[idx] = d
            idx += 1

    with open('rawdata.json', 'w') as f:
        json.dump(data, f, indent=2)

combine_raw_data()
