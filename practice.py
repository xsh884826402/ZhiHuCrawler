import re
from pymongo import MongoClient
import time
# basic_str = 'https://www.zhihu.com/api/v4/questions/317637620/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=10&offset=10&platform=desktop&sort_by=default'
# client = MongoClient('localhost',27017)
# db = client.ZhiHuCrawler
# collection_name = 'Answer_2019-4-1'
# collection = db[collection_name]
# dic = {}
# dic['str'] = 'str'
# collection.insert_one(dic)
pattern = re.compile(r'.*/questio(n|ns)/.*')
str = 'https://api.zhihu.com/questions/61772798'
str2 = 'https://api.zhihu.com/question/61772798'
print(pattern.match(str).group(1))