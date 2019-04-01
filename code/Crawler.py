#利用requesets 中的get方法爬取数据（利用cookies免登陆）
#link指定要爬取的链接，store_dir 指定存储的路径,Threshold 为过滤答案的阈值数
#对于返回的Json对象，可以使用"voteup_count": 4423,"comment_count": 566,字段来查找点赞数，content为答案的内容
import requests
from Crawler_Answer_for_each_Question import Crawler_Answer_for_each_Question
from bs4 import BeautifulSoup
def Crawler_Daily_hot(Threshold = 500):
    #知乎热榜url
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
        Dict_Item[item['href']] = item['title']
    print('Length',len(Hot_list),)

    print('--'*10,'开始爬取问题','--'*10)
    Crawler_Answer_for_each_Question(Dict_Item, headers, cookies)





if __name__ == "__main__":
    Crawler_Daily_hot()

#TopstoryContent > div > div > section:nth-child(2) > div.HotItem-content > a