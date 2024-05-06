import time
import requests
import csv
import numpy as np
import os
from datetime import datetime


def init():
    # 检查是否存在一个名为'navData.csv'的文件。如果文件不存在，它将创建一个新的CSV文件，
    # 并写入一行包含'typeName'，'gid'和'containerid'的标题
    if not os.path.exists('./articleData.csv'):
        with open('./articleData.csv', 'w', encoding='utf-8', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'id',
                'like_num',
                'comments_len',
                'reposts_count',
                'region',
                'content',
                'content_len',
                'created_at',
                'type',
                'detail_url',  # followBtnCode { followcardid+  uid }
                'author_avatar',
                'author_name',
                'author_detail',
                'is_vip'
            ])


def writer_row(row):
    # 爬出的数据添加到每一行
    # 接收一个参数row，并将其作为一行数据写入到'navData.csv'文件中
    with open('./articleData.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)


def get_data(url, params):
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
        return response.json()['statuses']
    else:
        return None


def get_all_type_list():
    type_list=[]
    with open('./navData.csv', 'r', encoding='utf-8', newline='') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)
        for row in reader:
            type_list.append(row)
        return type_list

def parse_json(response, type):
    for article in response:
        id = article['id']
        like_num = article['attitudes_count']
        comments_len = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于 ', '')
        except:
            region = '未知'
        content = article['text_raw']
        content_len = article['textLength']
        created_at = datetime.strptime(article['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
        type = type

        # 文章id + mblogid
        try:
            detail_url = "https://weibo.com/"+str(id)+'/'+str(article['mblogid'])
        except:
            detail_url = "none"
        author_avatar = article['user']['avatar_large']
        author_name = article['user']['screen_name']
        author_detail = article['user']['profile_url']
        is_vip = article['user']['v_plus']

        writer_row([
            id,
            like_num,
            comments_len,
            reposts_count,
            region,
            content,
            content_len,
            created_at,
            type,
            detail_url,
            author_avatar,
            author_name,
            author_detail,
            is_vip
        ])


def start(type_num = 3, page_num = 2):
    article_url = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    type_list = get_all_type_list()
    type_num_count = 0
    for type in type_list:
        if type_num_count >= type_num:
            return
        time.sleep(2)
        for page in range(0, page_num):
            print(f"[{datetime.now()}]: 正在爬取类型[{type[0]}]，第{page+1}页数据")
            time.sleep(1)
            params = {
                'groupid': type[1],
                'containerid': type[2],
                'max_id': page,
                'count': 10,
                'extparam': 'discover|new_feed'
            }
            response = get_data(article_url, params)
            parse_json(response, type[0])
        type_num_count += 1


if __name__ == '__main__':
    start()
