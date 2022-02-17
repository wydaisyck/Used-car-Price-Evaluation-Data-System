from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import json
from requests.exceptions import ProxyError


path = 'https://www.cars.com/for-sale/searchresults.action/?page=1&perPage=20&prMx=100000&rd=99999&searchSource=GN_REFINEMENT&sort=relevance&zc=90013'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/'
                  '605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
}

response = requests.get(path, headers=headers, timeout=30).content
soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
content = soup.html
make_list = content.find_all(class_='mkId')[0].ul

index_dict = dict()
make_url = 'https://www.cars.com/for-sale/searchresults.action/?mkId={mkid}&page=1&perPage=20&prMx=100000&rd=99999&searchSource=GN_REFINEMENT&sort=relevance&zc=90013'
for i in tqdm(range(1, len(make_list), 2)):
    name = eval(make_list.contents[i].contents[1]['data-dtm'])['value']
    while True:
        try:
            response = requests.get(make_url.format(mkid=int(make_list.contents[i].contents[1]['value'])), headers=headers, timeout=30).content
        except ProxyError:
            print('ProxyError:', "Spider restarted from last check point")
        else:
            break
    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
    content = soup.html
    try:
        model_list = content.find_all(class_='mdId')[0].ul
    except IndexError:
        continue
    model_res = list()
    for j in range(1, len(model_list), 2):
        model = eval(model_list.contents[j].contents[1]['data-dtm'])['value']
        model_res.append(model)
    index_dict[name] = model_res

