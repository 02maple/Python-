from snownlp import SnowNLP
import csv
import os
from utils.getPublicData import get_all_comments_data, get_all_article_data


def target_file():
    target_file = "target.csv"
    comments_list = get_all_comments_data()

    rate_data=[]
    good = 0
    bad = 0
    middle = 0

    for index, i in enumerate(comments_list):
        value = SnowNLP(i[4]).sentiments
        if value > 0.66:
            good += 1
            rate_data.append([i[4],  'good'])
        elif value < 0.45:
            bad += 1
            rate_data.append([i[4], 'bad'])
        else:
            middle += 1
            rate_data.append([i[4], 'middle'])

    for i in rate_data:
        with open(target_file, 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(i)


def main():
    target_file()


if __name__ == '__main__':
    main()