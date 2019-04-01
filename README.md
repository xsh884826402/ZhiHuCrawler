# 知乎爬虫入门

## 项目介绍
在目前信息量爆炸的社会，我们如何快速的筛选有效的高质量信息。   同时也为了学习下爬虫技术，我在这里写了简单的   **Python**
爬虫   爬虫主要由三个代码构成，分别是
- Crawler（爬取热榜的五十个问题）
- Crawler_search（搜索某个关键字，爬取该关键字相关的问题列表）
- Crawler_Answer_for_each_Question(针对问题列表，爬取该问题下面的全部高赞答案（按赞数筛选)
## 所用技术
- 数据库
  - Mongo
- 数据库访问
  - pymongo
- HTML解析
  -beautifulsoup
- Json解析
  - json（python自带）
- 获取相应
  - request     

***请自行安装依赖beautifulsoup，request，pymongo***
##使用方法
- 登录自己的知乎账号（推荐使用Chrome）
- 按F12，点击Network，然后刷新网页，此时会出现hot，将右侧的cookies拷贝到code文件夹下的cookies.txt文件中
- 可以按照需要，运行Crawler或者Crawler了


<image src="https://github.com/xsh884826402/ZhiHuCrawler/blob/master/TestingData/2.jpg" width=500>
