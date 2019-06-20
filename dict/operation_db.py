"""
    dict 数据库处理
    功能:提供服务端的所有数据库操作

"""
import pymysql
import hashlib

SALT = "#&AID_"  # 定义加密盐


class Database:
    def __init__(self, host='localhost',
                 port=3306,
                 user='root',
                 passwd='123456',
                 charset='utf8',
                 database='dict'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.database = database
        self.connect_db()  # 链接数据库

    # 连接数据库
    def connect_db(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        self.db.close()

    # 注册操作
    def register(self, name, passwd):
        sql = 'select * from user where name = "%s"' % name
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return False

        # 密码加密处理
        hash = hashlib.md5((name + SALT).encode())
        hash.update(passwd.encode())  # 算法加密
        passwd = hash.hexdigest()

        # 插入数据库
        sql = "insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    # 登录
    def login(self, name, passwd):
        hash = hashlib.md5((name + SALT).encode())
        hash.update(passwd.encode())  # 算法加密
        passwd = hash.hexdigest()
        sql = 'select * from user where name = "%s" and passwd = "%s"' % (name, passwd)
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return True
        else:
            return False

    # 查询单词
    def query(self, word):
        sql = 'select * from words where word = "%s"' % word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[2]

    # 插入历史记录
    def insert_history(self,name,word):
        sql="insert into hist (name,word) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception:
            self.db.rollback()

    # 查询历史记录
    def history(self,name):
        sql = "select name,word,time from hist where name = '%s' order by time desc limit 10"% name
        self.cur.execute(sql)
        return self.cur.fetchall()