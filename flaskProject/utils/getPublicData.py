from utils.query import query


def get_all_comments_data():
    comment_list = query("SELECT * FROM comment", [], 'select')
    return comment_list


def get_all_article_data():
    article_list = query("SELECT * FROM article", [], 'select')
    return article_list
