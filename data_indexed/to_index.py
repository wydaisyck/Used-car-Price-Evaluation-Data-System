import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from src.feature_engineering import *


files = os.listdir('res')
csv_list = list()
for i in files:
    if i[-3:] == 'csv':
        csv_list.append(i)

csv_sample = csv_list
for csv_file in tqdm(csv_sample):
    single_data_frame = pd.read_csv('res/' + csv_file)
    if csv_file == csv_list[0]:
        all_data_frame = single_data_frame
    else:
        all_data_frame = pd.concat([all_data_frame, single_data_frame], ignore_index=True)


for word in all_data_frame.make.unique():
    if not os.path.exists('data_indexed/' + word):
        os.mkdir('data_indexed/' + word)
    curr = all_data_frame[all_data_frame.make==word]

    for model_word in curr.model.unique():
        if not os.path.exists('data_indexed/' + word + '/' + model_word):
            os.mkdir('data_indexed/' + word + '/' + model_word)
        curr[curr.model == model_word].to_csv('data_indexed/' + word + '/' + model_word + '/data.csv')

