import numpy as np

from src.json2csv import get_numbers
import pandas as pd
import requests
import json


def find_lat_long(zipcode):
    url = 'http://api.zippopotam.us/us/{zipcode}'
    while True:
        try:
            api_info = requests.get(url.format(zipcode=int(zipcode))).json()
        except requests.exceptions.ProxyError:
            continue
        else:
            return api_info['places'][0]['longitude'], api_info['places'][0]['latitude']


def group_transmission(t_type, from_predict=False):
    if from_predict:
        to_digit_dict = {
            1: '<=6-speed automatic',
            0: '>6-speed automatic',
            2: 'other'
        }
        return to_digit_dict[t_type] if to_digit_dict.get(t_type) else 2
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
            0: 'fwd',
            1: '4wd',
            2: 'rwd',
            3: 'awd',
        }
        return to_digit_dict[d_str] if to_digit_dict.get(d_str) else 'other'
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
            0: 'beige',
            1: 'black',
            2: 'blue',
            3: 'brown',
            4: 'gold',
            5: 'gray',
            6: 'green',
            7: 'orange',
            8: 'purple',
            9: 'red',
            10: 'white',
            11: 'other'
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
            0: 'hybrid',
            1: 'e85 flex fuel',
            2: 'electric',
            3: 'diesel'
        }
        return to_digit_dict[f_str] if to_digit_dict.get(f_str) else 'gasoline'
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


def minute2pretty(num):
    if num < 60:
        return f'{int(num)} minutes'
    elif num < 1440:
        return '1 day'
    else:
        return f'{int(np.ceil(num/1440))} days'



def get_history(price):
    a = np.random.rand()
    crawler_start = 40 * 24 * 60
    crawler_proba = 0.5
    crawler_end = 40 * 24 * 60 - 60
    if a < crawler_proba:
        return minute2pretty(np.random.randint(crawler_end, crawler_start))
    else:
        return minute2pretty(np.random.randint(5, crawler_end))




def search_result(search_dict):
    make = search_dict['Make']
    model = search_dict['Model']

    min_year = 2000
    max_year = 2021
    min_mileage = 0
    max_mileage = 9999999
    max_price = 999999
    distance = 99999
    if search_dict.get('priceMax'):
        max_price = int(search_dict['priceMax'])
    if search_dict.get('minYear'):
        min_year = int(search_dict['minYear'])
    if search_dict.get('maxYear'):
        max_year = int(search_dict['maxYear'])
    if search_dict.get('minMileage'):
        min_mileage = int(search_dict['minMileage'])
    if search_dict.get('maxMileage'):
        max_mileage = int(search_dict['maxMileage'])
    if search_dict.get('distance'):
        distance = int(search_dict['distance'])

    target_df = pd.read_csv('data_indexed/'+make.lower()+'/'+model.lower()+'/'+'data.csv')
    target_df = target_df.drop(columns=target_df.columns[22:])
    target_df = target_df[(target_df.year <=max_year) & (target_df.year>=min_year)]
    target_df = target_df[(target_df.odometer<=max_mileage)]
    target_df = target_df[(target_df.odometer>=min_mileage)]
    target_df = target_df[target_df.price <= max_price]

    if search_dict.get('Exterior Color'):
        target_df = target_df[target_df['Exterior Color'].apply(lambda x: search_dict['Exterior Color'].lower() in str(x).lower())]
    if search_dict.get('Fuel Type'):
        target_df = target_df[target_df['Fuel Type'].apply(lambda x: search_dict['Fuel Type'].lower() == x.lower())]
    if search_dict.get('Drivetrain'):
        target_df['Drivetrain_tmp'] = target_df.Drivetrain.apply(group_drivetrain)
        target_df = target_df[target_df['Drivetrain_tmp'].apply(
            lambda x: search_dict['Drivetrain'].lower() == group_drivetrain(
                x, from_predict=True))]
    if search_dict.get('Transmission'):
        target_df['Transmission_tmp'] = target_df.Transmission.apply(group_transmission)
        target_df = target_df[target_df['Transmission_tmp'].apply(
            lambda x: search_dict['Transmission'].lower() == group_transmission(
                x, from_predict=True))]
    if search_dict.get('zipcode'):
        lon, lat = find_lat_long(search_dict['zipcode'])
        with open('search_car/zip_record.json') as f:
            one_data = json.load(f)
        sell_zip = target_df.seller_position.unique()
        dist_dict = dict()
        for one_zip in sell_zip:
            lon_car, lat_car = one_data[str(one_zip)]['longitude'], one_data[str(one_zip)]['latitude']
            dist_dict[one_zip] = (((float(lon_car)-float(lon)) * 55)**2 + ((float(lat_car)-float(lat)) * 69)**2)**0.5
        target_df['distance'] = target_df['seller_position'].apply(lambda x: dist_dict[x])
        target_df = target_df[target_df['distance']<=distance]
    target_df['update_history'] = target_df.price.apply(get_history)
    columns = ['price', 'year', 'odometer', 'Exterior Color', 'seller_name','seller_reviews_count', 'seller_rateing', 'City MPG', 'distance', 'update_history']
    target_df = target_df[columns]
    target_df = target_df.sort_values(by=['distance'])
    res_list = list()
    for i in target_df.iterrows():
        one_dict = dict()
        i = i[1].fillna('Unknown')
        for one_column in columns:
            one_dict[one_column] = None
        one_dict.update(dict(i))
        res_list.append(one_dict)
    return res_list

if __name__ == '__main__':
    test = {'zipcode': 90007, 'minYear': 2013, 'maxYear': 2018, 'priceMax': 40000, 'distance': 500, 'Exterior Color': 'Black', 'Make': 'Toyota', 'Model': 'Camry', 'Fuel Type': 'Gasoline', 'Drivetrain': 'FWD', 'Transmission': '>6-Speed AUTOMATIC', 'maxMileage': 50000, 'minMileage': 30000}
    search_result(test)