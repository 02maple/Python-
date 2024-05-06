import time
from urllib.parse import urlparse

import requests
import csv
import numpy as np
import os
from datetime import datetime


def init():
    # 检查是否存在一个名为'articleComment.csv'的文件。如果文件不存在，它将创建一个新的CSV文件，
    if not os.path.exists('./articleComment.csv'):
        with open('./articleComment.csv', 'w', encoding='utf-8', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'article_id',
                'created_at',
                'likes_counts',
                'region',
                'content',
                'author_name',
                'author_gender',
                'author_address',
                'author_avatar',
            ])


def writer_row(row):
    # 爬出的数据添加到每一行
    # 接收一个参数row，并将其作为一行数据写入到'navData.csv'文件中
    with open('./articleComment.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)


def get_response(url, params):
    # 接收一个URL作为参数，然后使用requests.get方法从该URL获取数据。
    # 使用一个包含Cookie和User-Agent的headers字典
    headers = {
        'Cookie': 'SINAGLOBAL=1917885289159.3245.1688538173984; PC_TOKEN=1f04c107d7; '
                  'login_sid_t=aa9919d66d2fb7bdf415fc1f183aa5c8; cross_origin_proto=SSL; _s_tentry=cn.bing.com; UOR=,'
                  ',cn.bing.com; Apache=2921530832889.7847.1714733420442; '
                  'ULV=1714733420444:2:1:1:2921530832889.7847.1714733420442:1688538173990; wb_view_log=1463*9151.75; '
                  'XSRF-TOKEN=EDV3Poc_E8Ddm9Rz_wmgRopf; '
                  'SUB=_2A25LMLU8DeRhGeFJ7VMY8yvEzjyIHXVoTEj0rDV8PUNbmtAGLVqgkW9Nf38i3WFQycxwymOV-V5KWTH2ZggxZvkS; '
                  'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFsB9KYYylj_ZEXmBiXJ9gm5JpX5KzhUgL.FoMNSo24e0'
                  '-RSK52dJLoI7L2IPiXw-xyUs2t; ALF=02_1717326445; '
                  'WBPSESS=VIMat820zjL5rTEoO9y5yZV0eyi6k8yJ_vQbu8oRkrzcFGlsne3C7d3k76JQCykyXc2eHaMol18yg7h65r4O7fG1o__jTwC5Jq9p4YUP10L3vJiokAebDDrFkjZ_yS8HS9mPoa2MK8mDIfffLz9iyw==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }
    time.sleep(1)

    # 实际运行时，发现会被微博的服务器关闭连接，由于请求过多
    # 所以这里加一个try except
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.ConnectionError:
        # 远程主机强制关闭了连接
        # 等待一段时间后，重新尝试发送HTTP请求
        print(f"[{datetime.now()}]: ConnectionError, waiting 8 seconds to retry")
        time.sleep(10)
        response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_article_id_from_url(url):
    # 接收一个URL作为参数，然后使用requests.get方法从该URL获取数据。
    # 使用一个包含Cookie和User-Agent的headers字典
    headers = {
        'Cookie': 'SINAGLOBAL=1917885289159.3245.1688538173984; PC_TOKEN=1f04c107d7; '
                  'login_sid_t=aa9919d66d2fb7bdf415fc1f183aa5c8; cross_origin_proto=SSL; _s_tentry=cn.bing.com; UOR=,'
                  ',cn.bing.com; Apache=2921530832889.7847.1714733420442; '
                  'ULV=1714733420444:2:1:1:2921530832889.7847.1714733420442:1688538173990; wb_view_log=1463*9151.75; '
                  'XSRF-TOKEN=EDV3Poc_E8Ddm9Rz_wmgRopf; '
                  'SUB=_2A25LMLU8DeRhGeFJ7VMY8yvEzjyIHXVoTEj0rDV8PUNbmtAGLVqgkW9Nf38i3WFQycxwymOV-V5KWTH2ZggxZvkS; '
                  'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFsB9KYYylj_ZEXmBiXJ9gm5JpX5KzhUgL.FoMNSo24e0'
                  '-RSK52dJLoI7L2IPiXw-xyUs2t; ALF=02_1717326445; '
                  'WBPSESS=VIMat820zjL5rTEoO9y5yZV0eyi6k8yJ_vQbu8oRkrzcFGlsne3C7d3k76JQCykyXc2eHaMol18yg7h65r4O7fG1o__jTwC5Jq9p4YUP10L3vJiokAebDDrFkjZ_yS8HS9mPoa2MK8mDIfffLz9iyw==',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
    }

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    user_id = path_parts[1]
    article_id_name = path_parts[2]
    get_id_url = f'https://weibo.com/ajax/statuses/show?id={article_id_name}&locale=zh-CN'

    response = requests.get(get_id_url, headers=headers)

    if response.status_code == 200:
        article_id = response.json()['id']
        comments_count = response.json()['comments_count']
        return article_id, comments_count
    else:
        return None, None


def parse_json(response, article_id):
    # 获取需要的值，存入csv
    for comment in response:
        created_at = datetime.strptime(comment['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
        likes_counts = comment['like_counts']
        try:
            region = comment['source'].replace('来自', '')
        except:
            region = '未知'
        content = comment['text_raw']
        author_name = comment['user']['screen_name']
        author_gender = comment['user']['gender']
        author_address = comment['user']['location']
        author_avatar = comment['user']['avatar_large']

        writer_row([
            article_id,
            created_at,
            likes_counts,
            region,
            content,
            author_name,
            author_gender,
            author_address,
            author_avatar
        ])


def start(page_num=2):
    url = input('请输入要爬取的微博文章链接: ')
    # 通过url获取文章id
    article_id, comments_count = get_article_id_from_url(url)
    print(f"[{datetime.now()}]: 文章ID:{article_id} 评论数量:{comments_count}")
    # 评论接口
    comment_url = 'https://weibo.com/ajax/statuses/buildComments'
    # 初始化
    init()
    print(f"[{datetime.now()}]: 文章ID:{article_id} 正在爬取评论")
    time.sleep(2)
    params = {
        # 按时间排序 微博按热度查询的评论数量有限制，无法完全爬取
        'flow': '1',
        'id': int(article_id),
        'is_show_bulletin': int(2),
        'max_id': '',
    }

    # 获取所有评论
    # max_id 的特殊处理，使其可以爬取所有的评论
    max_id = ''
    i = 0
    while max_id != 0:
        i += 1
        print(f"[{datetime.now()}]: 第{i}次评论爬取...... [max_id:{max_id}] ")
        response = get_response(comment_url, params)
        response_data = response['data']
        max_id = response['max_id']
        params['max_id'] = max_id
        parse_json(response_data, article_id)
    print(f"[{datetime.now()}]: 爬取评论结束 [max_id:{max_id}]")


if __name__ == '__main__':
    start()
