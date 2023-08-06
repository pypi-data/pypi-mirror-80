import urllib.request
import requests
from bs4 import BeautifulSoup

def get_html(u):
 headers = {
  'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
         AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'

 }  # 模拟浏览器访问
 response = requests.get(u,headers = headers)  # 请求访问网站
 html = response.text  # 获取网页源码
 return html  # 返回网页源码


def news():
 cy='https://cyx200902.github.io/xxlib/news.html'
 soup = BeautifulSoup(get_html(cy), 'lxml')  # 初始化BeautifulSoup库,并设置解析器
 get_html(cy)
 for li in soup.find_all(name='div'):  # 遍历父节点
  for a in li.find_all(name='a'):  # 遍历子节点
   if a.string == None:
      pass
   else:
      print(a.string)  # 输出结果



news()