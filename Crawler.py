#利用requesets 中的get方法爬取数据（利用cookies免登陆）
#link指定要爬取的链接，store_dir 指定存储的路径,Threshold 为过滤答案的阈值数
#对于返回的Json对象，可以使用"voteup_count": 4423,"comment_count": 566,字段来查找点赞数，content为答案的内容
import requests
import re
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
def Crawler():
    Threshold = 500
    #MongoDB Created
    client = MongoClient(host='localhost', port =27017)
    db = client.ZhiHuCrawler
    collection = db.Answer
    #ZhiHuAnswer_address 模板 addresss_0 + questionid +address_1 +limit=10&offset=10 +addresss_2
    ZhiHuAnswer_address_0 = 'https://www.zhihu.com/api/v4/questions/'
    ZhiHuAnswer_address_1 = '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&'
    ZhiHuAnswer_address_2 = '&platform=desktop&sort_by=default'
    link = "https://www.zhihu.com/hot"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    cookies = {}
    with open('./cookies.txt', 'r') as f:
        for line in f.readline().split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value

    res = requests.get(link, headers=headers, cookies=cookies)
    print("热榜status", res.status_code)

    with open('1.html', 'w', encoding='utf-8') as f:
        f.write(res.text)

    soup = BeautifulSoup(res.text, features='lxml')
    Hot_list = soup.select('#TopstoryContent > div > div > section > div.HotItem-content > a')

    #Dict_Item 存储所有的热点问题，共五十个，key='问题描述',value = 'href'
    Dict_Item = {}
    for item in Hot_list:
        Dict_Item[item['title']] = item['href']
    print('Length',len(Hot_list),)

    print('--'*10,'开始爬取问题','--'*10)

    pattern = re.compile(r'.*/question/(\d+)')
    for key , value in Dict_Item.items():
        time.sleep(10)
        print('key',key,"Value",value)
        question_id = pattern.match(value).group(1)
        # address 是通用的地址，后面的tmp才是真正的地址
        address = ZhiHuAnswer_address_0 + question_id + ZhiHuAnswer_address_1
        limit = 5
        offset = 0
        print('--'*10,'开始爬取')
        while(True):
            time.sleep(2)
            li_off_str = 'limit=5&offset=' + str(offset)
            tmp = address + li_off_str + ZhiHuAnswer_address_2
            offset += 5
            answer_res = requests.get(tmp, headers=headers,cookies = cookies)
            content = json.loads(answer_res.text)
            if len(content['data']) == 0:
                break
            #m每个item 为一个回答
            for item in content['data']:
                if item['voteup_count'] >= 500:
                    dic = {}
                    dic['question'] = item['question']
                    dic['author'] = item['author']
                    dic['answer_url'] = item['url']
                    dic['voteup_count'] = item['voteup_count']
                    dic['content'] = item['content']
                    collection.insert_one(dic)

            # print('Answer', type(answer_res),answer_res.text)

        # print(soup.prettify())
        # print('Answer_res StatusCode',answer_res.status_code)
        # with open('2.html', 'w', encoding='utf-8') as f:
        #     f.write(answer_res.text)

if __name__ == "__main__":
    Crawler()

#TopstoryContent > div > div > section:nth-child(2) > div.HotItem-content > a