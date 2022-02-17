import time
import json
from numpy import random as np_random


def get_time():
    time_str = time.strftime("%Y-%m-%d %X")
    return time_str


def get_updated():
    updated = str(round(np_random.poisson(lam=8)))
    return updated


def find_model(make):
    with open('car_index2.json', 'r') as rf:
        car = json.load(rf)
    car[""] = []
    model_list = car[make]
    return model_list


def process_dict(raw_dict):
    res_dict = {k: v for k, v in raw_dict.items() if v != '0'}
    res_dict = {k: v for k, v in res_dict.items() if v != 0}
    return res_dict


def search_dict(dict):
    if 'searchMileage' in dict.keys():
        dict["maxMileage"] = dict["searchMileage"]
        if dict["searchMileage"] == 30000:
            dict["minMileage"] = 1
        elif dict["searchMileage"] == 50000:
            dict["minMileage"] = 30001
        elif dict["searchMileage"] == 100000:
            dict["minMileage"] = 50001
        elif dict["searchMileage"] == 150000:
            dict["minMileage"] = 100001
        elif dict["searchMileage"] == 300000:
            dict["minMileage"] = 150001
        dict.pop('searchMileage')
    return dict


def convert_array(c):
    key = ["2021", "2022", "2023", "2024", "2025"]
    c = c.astype(int)  # 调用预测函数
    val = c.tolist()
    res = dict(zip(key, val))
    return res


if __name__ == '__main__':
    print(get_time())
    print(read_json())




