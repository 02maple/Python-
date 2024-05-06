from snownlp import SnowNLP
import csv
import os
import pandas as pd
from datetime import datetime


def sentiment_analysis():

    target_file = "sentimentAnalysis.csv"
    df = pd.read_csv('../spiders/articleComment.csv')
    comments_list = df['content'].values

    rate_data = []
    good = 0
    bad = 0
    middle = 0

    print(f"[{datetime.now()}]: 正在进行情感分析......")
    for index, i in enumerate(comments_list):
        value = SnowNLP(i).sentiments
        if value > 0.66:
            good += 1
            rate_data.append([i, 'good'])
        elif value < 0.45:
            bad += 1
            rate_data.append([i, 'bad'])
        else:
            middle += 1
            rate_data.append([i, 'middle'])

    for i in rate_data:
        with open(target_file, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(i)
    print(f"[{datetime.now()}]: 情感分析结束")


def main():
    sentiment_analysis()


if __name__ == '__main__':
    main()
