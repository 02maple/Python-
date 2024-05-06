from utils.getPublicData import get_all_comments_data, get_all_article_data
import jieba
import jieba.analyse as analyse
target_txt = 'cutComments.txt'


def stop_words():
    with open('./stopwords_cn.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]


def seg_depart(sentence):
    sentence_depart = jieba.cut(' '.join([x[4] for x in sentence]).strip())
    stop_words_list = stop_words()
    out_str = ''
    for word in sentence_depart:
        if word not in stop_words_list:
            if word != '\t':
                out_str += word
    return out_str



def writer_comments_cuts():
    with open(target_txt, 'a+', encoding='utf-8') as target_file:
        seg = jieba.cut(seg_depart(get_all_comments_data()), cut_all=True)
        out_put = ''.join(seg)
        target_file.write(out_put)
        target_file.write('\n')


if __name__ == '__main__':
    writer_comments_cuts()
