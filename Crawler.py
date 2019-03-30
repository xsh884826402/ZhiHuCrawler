#利用requesets 中的get方法爬取数据（利用cookies免登陆）
#link指定要爬取的链接，store_dir 指定存储的路径,Threshold 为过滤答案的阈值数
import requests
import re
from bs4 import BeautifulSoup
def Crawler():
    link = "https://www.zhihu.com/hot"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    cookies = {}
    with open('./cookies.txt', 'r') as f:
        for line in f.readline().split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value
    res = requests.get(link, headers=headers, cookies=cookies)
    print(res.status_code)
    # print(res.text)
    with open('1.html', 'w', encoding='utf-8') as f:
        f.write(res.text)
    soup = BeautifulSoup(res.text, features='lxml')
    # print(soup.prettify())
    Hot_list = soup.find_all('a',{'href': re.compile('http.*'),'title': re.compile('.*')})
    Hot_item = soup.find_all('section',{'class':'HotItem'})
    print("Lengthof Hot Item",len(Hot_item))
    Item = []
    for item in Hot_list:
        Item.append(item['title'])
    print('Length',len(Hot_list),len(Item))
    print(Item)

if __name__ == "__main__":
    Crawler()