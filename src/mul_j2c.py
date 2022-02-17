from src.json2csv import *
from multiprocessing import Pool
import os

if __name__ == '__main__':

    pool = Pool(processes=34)

    files = os.listdir('data_json_fined')

    json_list = list()
    for i in files:
        if i[-4:] == 'json':
            json_list.append(i)
    batches = [[] for _ in range(34)]

    for i, one_item in enumerate(json_list):
        batches[i%34].append(one_item)
    pool.map(j2c, batches)