from pymysql import *

connect = connect(host='118.89.116.89', port=3306, user='root', password='Zsj20021012!', database='weiboarticles')
cursor = connect.cursor()

def query(sql, params, type = "no select"):
    params = tuple(params)
    cursor.execute(sql, params)
    connect.ping(reconnect=True)
    # 查询走if条件
    if type != "no select":
        data_list = cursor.fetchall()
        connect.commit()
        return data_list
    else:
        connect.commit()



