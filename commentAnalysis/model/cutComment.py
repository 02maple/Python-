import jieba
import jieba.analyse as analyse
import pandas as pd
from datetime import datetime
target_txt = 'cutComments.txt'


def stop_words():
    with open('./stopwords_cn.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]


def seg_depart(sentence):
    sentence_depart = jieba.cut(' '.join([x for x in sentence]).strip())
    stop_words_list = stop_words()
    out_str = ''
    for word in sentence_depart:
        if word not in stop_words_list:
            if word != '\t':
                out_str += word
    return out_str


def writer_comments_cuts():
    with open(target_txt, 'a+', encoding='utf-8') as target_file:
        df = pd.read_csv('../spiders/articleComment.csv')
        comment_data = df['content'].values
        print(f"[{datetime.now()}]: 正在分词......")
        # False 使用精确模式进行分词，精确模式是试图将句子最精确地切开，适合文本分析
        seg = jieba.cut(seg_depart(comment_data), cut_all=False)
        out_put = ''.join(seg)
        target_file.write(out_put)
        target_file.write('\n')
        print(f"[{datetime.now()}]: 分词结束")


if __name__ == '__main__':
    writer_comments_cuts()
