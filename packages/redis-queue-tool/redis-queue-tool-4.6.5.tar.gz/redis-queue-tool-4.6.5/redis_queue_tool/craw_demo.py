# -*- coding: utf-8 -*-
# @Time    : 2020/8/22 14:55
# @Author  : CC
# @Desc    : craw_demo.py 使用框架爬取某个平台数据demo
from gevent import monkey

monkey.patch_all()

from lxml import etree
import requests
from redis_queue_tool import task_deco, MiddlewareEum


@task_deco('douban:top250', qps=10, customer_type='gevent', middleware=MiddlewareEum.MEMORY)
def get_douban_top250(page: int = 0):
    url = f"https://movie.douban.com/top250?start={page * 25}&filter="

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Cookie': 'bid=hnhTI11clY0'
    }

    response = requests.request("GET", url, headers=headers)

    html = etree.HTML(response.text)
    movies = html.xpath('//ol[@class="grid_view"]/li')
    for movie in movies:
        item = dict()
        item['ranking'] = movie.xpath(
            './/div[@class="pic"]/em/text()')[0]
        item['movie_name'] = movie.xpath(
            './/div[@class="hd"]/a/span[1]/text()')[0]
        item['score'] = movie.xpath(
            './/div[@class="star"]/span[@class="rating_num"]/text()'
        )[0]
        print(item)


if __name__ == '__main__':
    # 发布任务
    for i in range(1, 11):
        get_douban_top250.pub(i)

    # 消费任务
    get_douban_top250.start()
