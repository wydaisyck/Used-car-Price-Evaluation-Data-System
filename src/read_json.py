import json
import os
import re
from tqdm import tqdm
from collections import Counter


def to_json_batch():
    files = os.listdir('car_data')
    json_list = list()
    for i in files:
        if i[-4:] == 'json':
            json_list.append(i)

    save_count = 0
    index = 0
    new_dict = dict()
    with open('../model/model_constants/important_features.txt', 'r') as f:
        sig_fea = f.readlines()
    sig_fea = eval(sig_fea[0])
    for i in tqdm(json_list):
        save_count += 1

        with open('car_data/'+i) as f:
            one_data = json.load(f)

        for key in one_data:
            new_dict[int(key)] = dict()
            new_dict[int(key)].update(one_data[key]['vehicle_head_info'])
            new_dict[int(key)].update(one_data[key]['seller_info'])
            new_dict[int(key)].update(one_data[key]['basics'])
            new_dict[int(key)].update({
                'all_features': list(set(sig_fea).intersection(set(one_data[key]['all_features'])))
            })


        if save_count == 10:
            with open("data/batch_{index}.json".format(index=index), "w") as jsonfile:
                json.dump(new_dict, jsonfile, ensure_ascii=False)
            index += 1
            save_count = 0
            new_dict = dict()
    else:
        with open("data/batch_{index}.json".format(index=index), "w") as jsonfile:
            json.dump(new_dict, jsonfile, ensure_ascii=False)
    print('done!')


def find_make_model(title):
    index_key = list(index_data.keys())
    for make in index_key:
        if make.lower() in title.lower():
            car_make = make.lower()
            for model in index_data[make]:
                if model.lower() in title.lower():
                    car_model = model.lower()
                    date = re.search(r"\d{4}", title).group(0)
                    return date, car_make, car_model
    else:
        return None


if __name__ == '__main__':
    # to_json_batch()
    files = os.listdir('data')
    json_list = list()
    for i in files:
        if i[-4:] == 'json':
            json_list.append(i)

    with open("../model/model_constants/car_index.json", "r") as f:
        index_data = json.load(f)

    for i in tqdm(json_list):
        with open('data/' + i) as f:
            one_data = json.load(f)
        one_data_key = list(one_data.keys())
        for car_index in one_data_key:
            if one_data[car_index]['title']:
                res = find_make_model(one_data[car_index]['title'])
                if res:
                    year_one_car, make_one_car, model_one_car = res
                    one_data[car_index].update({
                        'year': year_one_car,
                        'make': make_one_car,
                        'model': model_one_car
                    })
                    one_data[car_index].pop('title')
                else:
                    one_data.pop(car_index)
            else:
                one_data.pop(car_index)
        with open("data_json_fined/"+i, "w") as jsonfile:
            json.dump(one_data, jsonfile, ensure_ascii=False)
