import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from src.json2csv import get_numbers


def group_transmission(t_type, from_predict=False):
    if from_predict:
        to_digit_dict = {
            '<=6-speed automatic': 1,
            '>6-speed automatic': 0,
            'other': 2
        }
        return to_digit_dict[t_type.lower()] if to_digit_dict.get(t_type.lower()) else 2
    else:
        if type(t_type) == str and 'auto' in t_type.lower():
            if get_numbers(t_type):
                if get_numbers(t_type) >= 7:
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 2


def group_drivetrain(d_str, from_predict=False):
    if from_predict:
        to_digit_dict = {
            'fwd': 0,
            '4wd': 1,
            'rwd': 2,
            'awd': 3,
        }
        return to_digit_dict[d_str.lower()] if to_digit_dict.get(d_str.lower()) else 4
    else:
        if type(d_str) == str:
            if d_str == 'FWD' or 'front' in d_str.lower():
                return 0
            elif d_str == '4WD' or 'four' in d_str.lower() or '4' in d_str:
                return 1
            elif d_str == 'RWD' or 'rear' in d_str.lower():
                return 2
            elif d_str == 'AWD' or 'all' in d_str.lower():
                return 3
            else:
                return 4
        else:
            return 4


def group_color(d_str, from_predict=False):
    if from_predict:
        to_dict = {
            'beige': 0,
            'black': 1,
            'blue': 2,
            'brown': 3,
            'gold': 4,
            'gray': 5,
            'green': 6,
            'orange': 7,
            'purple': 8,
            'red': 9,
            'white': 10,
            'other': 11
        }
        return to_dict[d_str.lower()]
    else:
        if type(d_str) == str:
            if 'beige' in d_str.lower():
                return 0
            elif 'black' in d_str.lower():
                return 1
            elif 'blue' in d_str.lower():
                return 2
            elif 'brown' in d_str.lower():
                return 3
            elif 'gold' in d_str.lower():
                return 4
            elif 'gray' in d_str.lower():
                return 5
            elif 'green' in d_str.lower():
                return 6
            elif 'orange' in d_str.lower():
                return 7
            elif 'purple' in d_str.lower():
                return 8
            elif 'red' in d_str.lower():
                return 9
            # elif 'sliver' in d_str.lower():
            #     return 10
            elif 'white' in d_str.lower():
                return 10
            else:
                return 11
        else:
            return 11


def group_fuel_type(f_str, from_predict=False):

    if from_predict:
        to_digit_dict = {
            'hybrid': 0,
            'e85 flex fuel': 1,
            'electric': 2,
            'diesel': 3
        }
        return to_digit_dict[f_str.lower()] if to_digit_dict.get(f_str.lower()) else 4
    else:
        if f_str == 'Hybrid':
            return 0
        elif f_str == 'E85 Flex Fuel':
            return 1
        elif f_str == 'Electric':
            return 2
        elif f_str == 'Diesel':
            return 3
        else:
            return 4


def group_make(mk_str):
    return make_dict[mk_str.lower()]


def group_model(md_str):
    return model_dict[md_str.lower()]


if __name__ == '__main__':
    files = os.listdir('res')

    csv_list = list()
    for i in files:
        if i[-3:] == 'csv':
            csv_list.append(i)

    csv_sample = csv_list
    for csv_file in tqdm(csv_sample):
        single_data_frame = pd.read_csv('res/'+csv_file)
        if csv_file == csv_list[0]:
            all_data_frame = single_data_frame
        else:
            all_data_frame = pd.concat([all_data_frame, single_data_frame], ignore_index=True)

    columns = ['key', 'year', 'make', 'model', 'odometer',
               'Transmission', 'Drivetrain', 'Interior Color', 'Exterior Color',
               'City MPG', 'Highway MPG', 'Fuel Type', 'seller_position',
               'seller_reviews_count', 'seller_rateing', 'price', 'seller_name', 'VIN',
               'Engine displacement', 'cylinder', 'Braking Assist', 'Passenger Airbag',
               'Tachometer', 'ABS and Driveline Traction Control']

    with open("car_index.json", "r") as f:
        index_data = json.load(f)

    make_dict = dict()
    for i, make in enumerate(index_data.keys()):
        make_dict[make.lower()] = i

    model_values = list()
    for value_list in index_data.values():
        model_values += value_list

    model_dict = dict()
    for i, model in enumerate(model_values):
        model_dict[model.lower()] = i


    all_data_frame = pd.read_csv('data_dropna.csv')


    fre_model = list(all_data_frame.model.value_counts().index[:200])
    all_data_frame.model = all_data_frame.model.apply(lambda x: x if x in fre_model else -1)
    data_df = pd.get_dummies(all_data_frame, columns=['year', 'make', 'model',
           'Transmission', 'Drivetrain', 'Interior Color', 'Exterior Color',
                                                      'Fuel Type','cylinder'])
    features = data_df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'key', 'seller_position',
                                     'seller_name', 'VIN', 'price'])

    tozs_features = [
        'odometer', 'City MPG',
        'Highway MPG', 'seller_reviews_count',
        'seller_rateing', 'Engine displacement'
    ]
    for one_feature in tozs_features:
        features[one_feature] = (features[one_feature]-features[one_feature].mean())/(features[one_feature].std())
    np.save('label.npy', data_df.price.to_numpy())
