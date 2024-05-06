import jieba
import wordcloud
from datetime import datetime


# 读取文本

def generate_word_cloud():
    with open("cutComments.txt", encoding="utf-8") as f:
        s = f.read()
    ls = jieba.lcut(s)  # 生成分词列表
    text = ' '.join(ls)  # 连接成字符串

    print(f'[{datetime.now()}]: 正在生成词云图......')
    wc = wordcloud.WordCloud(font_path="msyh.ttc",
                             width=1000,
                             height=700,
                             background_color='white',
                             max_words=100, stopwords=s)
    # msyh.ttc电脑本地字体，写可以写成绝对路径
    wc.generate(text)  # 加载词云文本
    wc.to_file("wordCloud.png")  # 保存词云文件
    print(f'[{datetime.now()}]: 生成词云图结束')


if __name__ == '__main__':
    generate_word_cloud()
