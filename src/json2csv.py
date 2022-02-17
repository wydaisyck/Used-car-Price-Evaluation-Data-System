import pandas as pd
import json
import os
from tqdm import tqdm

def get_numbers(a_str):
    if a_str:
        number_str = ''
        for one_letter in a_str:
            if one_letter.isdigit():
                number_str += one_letter
        return float(number_str) if number_str.isdigit() else None
    else:
        return None


def get_edp(a_str):
    if a_str:
        if ' L' in a_str:
            head = a_str[:a_str.index(' L')]
            return get_numbers(head.split(' ')[-1])
        elif 'L' in a_str:
            head = a_str[:a_str.index('L')]
            return get_numbers(head.split(' ')[-1])
        else:
            return None
    else:
        return None

def get_ec(a_str):
    if a_str:
        engine_data = a_str.split(' ')
        for data in engine_data:
            if data[0] == 'V' or data[0] == 'I' or data[0] == 'v' or data[0] == 'i':
                res = get_numbers(data)
                if res:
                    return res
                else:
                    continue
    else:
        return None

def j2c(json_list):
    # json_list = list()
    # for i in files:
    #     if i[-4:] == 'json':
    #         json_list.append(i)
    print(len(json_list))
    with open('important_features.txt', 'r') as f:
        sig_fea = f.readlines()
    sig_fea = eval(sig_fea[0])

    for json_file in tqdm(json_list):
        df = pd.DataFrame()
        with open('data_json_fined/' + json_file, mode='r', encoding='UTF-8') as f:
            one_data = json.load(f)
        for one_car in one_data:
            one_car_data = {
                'key': one_car,
                'year': int(one_data[one_car].get('year')),
                'make': one_data[one_car].get('make'),
                'model': one_data[one_car].get('model'),
                'odometer': get_numbers(one_data[one_car].get('odometer')),
                'Transmission': one_data[one_car].get('Transmission'),
                'Drivetrain': one_data[one_car].get('Drivetrain'),
                'Interior Color': one_data[one_car].get('Interior Color'),
                'Exterior Color': one_data[one_car].get('Exterior Color'),
                'City MPG': get_numbers(one_data[one_car].get('City MPG')),
                'Highway MPG': get_numbers(one_data[one_car].get('Highway MPG')),
                'Fuel Type': one_data[one_car].get('Fuel Type'),
                'seller_position': get_numbers(one_data[one_car].get('seller_position')),
                'seller_reviews_count': get_numbers(one_data[one_car].get('seller_reviews_count')),
                'seller_rateing': get_numbers(one_data[one_car].get('seller_rateing')),
                'price': get_numbers(one_data[one_car].get('price')),
                'seller_name': one_data[one_car].get('seller_name'),
                'VIN': one_data[one_car].get('VIN'),
                'Engine displacement': get_edp(one_data[one_car].get('Engine')),
                'cylinder': get_ec(one_data[one_car].get('Engine'))
            }
            for fea in sig_fea:
                one_car_data.update({
                    fea: 1 if fea in one_data[one_car]['all_features'] else 0
                })
            df = df.append([one_car_data])
        df.to_csv('res/'+json_file[:-4]+'csv')


