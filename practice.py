import  requests
# session = requests.session()
# from bs4 import BeautifulSoup
# import lxml
#
link = "https://www.zhihu.com/hot"
# postdata = {
#     'username' : '13051191950',
#     'password' : 'mima2161228'
# }
headers  = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# # login_page = session.post(link,data= postdata, headers=headers)
# re = requests.get(link, headers=headers)
# print(re.status_code)
# print(re.text)
# with open('./1.html','w',encoding='utf-8') as f:
#     f.write(re.text)
cookies = {}
with open('./cookies.txt','r') as f:
    for line in f.readline().split(';'):
        name, value = line.strip().split('=',1)
        cookies[name] = value
# print(cookies)
res = requests.get(link,headers=headers,cookies=cookies)
print(res.status_code)
# print(res.text)
with open('1.html','w',encoding='utf-8') as f:
    f.write(res.text)
