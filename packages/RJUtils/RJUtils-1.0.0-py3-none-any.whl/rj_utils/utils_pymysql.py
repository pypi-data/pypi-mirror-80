import pymysql
from pymysql.cursors import DictCursor

"""
pymysql
"""


class DBUtils:
    conn = None
    cur = None

    def initConnect(self):
        try:
            # 创建数据库连接  localhost等效于127.0.0.1
            self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="bigdata",
                                        charset="utf8")
            # 建立游标，指定游标类型，返回字典
            self.cur = self.conn.cursor(DictCursor)
        except:
            print("连接数据库异常")

    def exec_select(self, sqlStr):
        try:
            # 操作语句，只查询前两行 'select * from students limit 2;'
            self.cur.execute(sqlStr)
            # 获取查询的所有结果
            res = self.cur.fetchall()
            # 打印结果
            # print(res)
            return res
        except:
            print("执行异常")
            return None

    def exec(self, sqlStr):
        try:
            # 操作语句，只查询前两行 'select * from students limit 2;'
            self.cur.execute(sqlStr)
        except:
            print("执行异常")

    def closeConnect(self):
        try:
            # 关闭游标
            self.cur.close()
            # 关闭连接
            self.conn.close()
        except:
            print("执行异常")


if __name__ == '__main__':
    db = DBUtils()
    db.initConnect()
    db.exec('select * from strategies;')
