import jieba
import re


def main():
    reader = open('./cutComments.txt', 'r', encoding='utf-8')
    start = reader.read()
    result = open('./wordFrequency.csv', 'w', encoding='utf-8')

    # 分词，去重生成列表
    # 使用 jieba 库的 cut 函数对 start 中的文本进行分词处理。
    # cut_all=True 表示使用全模式分词，即尽可能将文本切分为多个词语
    word_list = jieba.cut(start, cut_all=False)
    new_words = []
    for i in word_list:
        # 使用正则表达式查找词语 i 中是否包含数字。
        # 如果包含，m 将是一个匹配对象；否则，m 将是 None
        m = re.search("\d", i)

        # 使用正则表达式查找词语 i 中是否包含非字母数字字符。
        # 如果包含，n 将是一个匹配对象；否则，n 将是 None
        n = re.search("\W", i)
        if not m and not n and len(i) > 1:
            new_words.append(i)

    # 统计词频
    word_count = {}
    for word in set(new_words):
        word_count[word] = new_words.count(word)

    # 格式整理
    list_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    for i in range(100):
        print(list_count[i], file=result)


if __name__ == '__main__':
    main()
