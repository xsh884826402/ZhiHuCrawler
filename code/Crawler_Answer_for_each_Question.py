from pymongo import MongoClient
import time
import re
import requests
import json
def Crawler_Answer_for_each_Question(Dict_Item: dict,headers: dict, cookies: dict, Threshold = 300):
    # ZhiHuAnswer_address 模板 addresss_0 + questionid +address_1 +limit=10&offset=10 +addresss_2
    ZhiHuAnswer_address_0 = 'https://www.zhihu.com/api/v4/questions/'
    ZhiHuAnswer_address_1 = '/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&'
    ZhiHuAnswer_address_2 = '&platform=desktop&sort_by=default'

    # MongoDB Created
    client = MongoClient(host='localhost', port=27017)
    db = client.ZhiHuCrawler
    localtime = time.localtime(time.time())
    mon,day = localtime.tm_mon, localtime.tm_mday
    collection_name = 'Answer_' + str(mon) +'_'+ str(day)
    collection = db[collection_name]

    pattern = re.compile(r'.*/questio.*?/(\d+)')
    for key , value in Dict_Item.items():
        time.sleep(10)
        print('key',key,"Value",value)
        question_id = pattern.match(key).group(1)
        # address 是通用的地址，后面的tmp才是真正的地址
        address = ZhiHuAnswer_address_0 + question_id + ZhiHuAnswer_address_1
        limit = 5
        offset = 0
        print('--'*10,'开始爬取')
        while(True):
            time.sleep(3)
            li_off_str = 'limit=5&offset=' + str(offset)
            tmp = address + li_off_str + ZhiHuAnswer_address_2
            offset += 5
            answer_res = requests.get(tmp, headers=headers,cookies = cookies)
            content = json.loads(answer_res.text)
            if len(content['data']) == 0:
                break
            #m每个item 为一个回答
            count_continuous_no_insert = 0
            for item in content['data']:
                if count_continuous_no_insert >= 20:
                    break
                if item['voteup_count'] >= Threshold:
                    dic = {}
                    dic['question'] = item['question']
                    dic['author'] = item['author']
                    dic['answer_url'] = item['url']
                    dic['voteup_count'] = item['voteup_count']
                    dic['content'] = item['content']
                    collection.insert_one(dic)
                    print('--'*10,'插入数据库')
                else:
                    count_continuous_no_insert += 1