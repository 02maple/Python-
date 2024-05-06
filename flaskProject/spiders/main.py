from spiderContent import start as spiderContentStart
from spiderComment import start as spiderCommentStart
from datetime import datetime
import os
from sqlalchemy import create_engine
import pandas as pd

# 数据库连接对象
engine = create_engine('mysql+pymysql://root:Zsj20021012!@118.89.116.89:3306/weiboarticles?charset=utf8mb4')


def save_to_sql():
    article_new_pd = pd.read_csv('./articleData.csv', header=None)
    comment_new_pd = pd.read_csv('./articleComment.csv', header=None)
    article_new_pd.to_sql('article', con=engine, if_exists='replace', index=False)
    comment_new_pd.to_sql('comment', con=engine, if_exists='replace', index=False)


def main():
    print(f"[{datetime.now()}] Start crawling Weibo article data...")
    spiderContentStart(4, 2)
    print(f"[{datetime.now()}] Start crawling Weibo comment data...")
    spiderCommentStart()
    print(f"[{datetime.now()}] Start saving data to MySQL...")
    save_to_sql()


if __name__ == '__main__':
    save_to_sql()
