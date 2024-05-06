import time
from datetime import datetime
import requests
import csv
import numpy as np
import os

# 爬取热门微博导航栏菜单数据


def init():
    # 检查是否存在一个名为'navData.csv'的文件。如果文件不存在，它将创建一个新的CSV文件，
    # 并写入一行包含'typeName'，'gid'和'containerid'的标题
    if not os.path.exists('./navData.csv'):
        with open('./navData.csv', 'w', encoding='utf-8', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'typeName',
                'gid',
                'containerid'
            ])


def writerRow(row):
    # 爬出的数据添加到每一行
    # 接收一个参数row，并将其作为一行数据写入到'navData.csv'文件中
    with open('./navData.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)


def get_data(url):
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
    # 包含两个参数（'is_new_segment'和'fetch_hot'）的params字典
    params = {
        'is_new_segment': 1,
        'fetch_hot': 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def parse_json(response):
    # 当前获取的结果并不完整，我们需要进一步处理数据，以便将其写入到CSV文件中
    # 使用numpy的append函数将response['groups'][3]['group']和response['groups'][4]['group']两部分数据合并到一起
    nav_list = np.append(response['groups'][3]['group'], response['groups'][4]['group'])
    # 将这个列表作为一行数据写入到 'navData.csv' 文件中
    for nav in nav_list:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        writerRow([navName, gid, containerid])
    print(f"[{datetime.now()}]: 微博榜单数据已经写入navData.csv文件中，执行成功！")


if __name__ == '__main__':
    init()
    url = 'https://weibo.com/ajax/feed/allGroups'
    # 获取需要使用的内容，存入csv中，各个榜单需要使用typename,gid,containerid
    response = get_data(url)
    parse_json(response)
