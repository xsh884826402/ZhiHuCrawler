#通过关键字搜索，将关键字放入特定的url方法中，通过调整offset不断获取相应的问题，最终得到一个question list
#url:https://www.zhihu.com/api/v4/search_v3?t=general&q=%E8%AE%A1%E7%AE%97%E6%9C%BA&correction=1&offset=0&limit=20&lc_idx=26&show_all_topics=0&search_hash_id=c37c1498c14f6cac0e3043d239fd3cb9&vertical_info=2%2C1%2C1%2C1%2C0%2C1%2C0%2C1%2C0%2C1
#返回一个关键字问题下对应的所有列表
import requests
from bs4 import BeautifulSoup
import time
import json
from Crawler_Answer_for_each_Question import Crawler_Answer_for_each_Question
def Crawler_search(keyword):
    #address = address_0 + 'keyword' + address_1  + '偏移量' + address_2
    address_0 = 'https://www.zhihu.com/api/v4/search_v3?t=general&q='
    address_1 = '&correction=1&offset='
    address_2 = '&limit=20&lc_idx=26&show_all_topics=0&search_hash_id=c37c1498c14f6cac0e3043d239fd3cb9&vertical_info=2%2C1%2C1%2C1%2C0%2C1%2C0%2C1%2C0%2C1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    cookies = {}
    with open('./cookies.txt', 'r') as f:
        for line in f.readline().split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value
    offset = 0
    dic_question_list = {}
    print('Before While')
    count = 0
    while(True):
        time.sleep(4)
        url = address_0 + keyword + address_1 + str(offset) + address_2
        print('URL',url)
        res = requests.get(url=url, headers=headers,cookies=cookies)
        print('Status_code',res.status_code)
        content = json.loads(res.text)
        if count >=10:
            break
        count += 1
        if len(content) == 0:
            print('None')
            break
        offset += 20
        for item in content['data']:
            if 'object' in item.keys():
                if 'question' in item['object'].keys() :
                    dic_question_list[item['object']['question']['url']] = " "

    print('__'*10,'已获取到关键字',keyword,'下的所有答案列表','__'*10)
    return dic_question_list,headers,cookies


if __name__ == "__main__":
    print('请输入关键字:')
    key = input()
    print('按多少赞筛选：')
    Threshold = input()
    # print(key)
    dic,headers,cookies = Crawler_search(key)
    print(dic.keys())
    Crawler_Answer_for_each_Question(dic, headers,cookies,Threshold=int(Threshold))
