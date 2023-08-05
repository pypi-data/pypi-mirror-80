import datetime
import pymysql


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton


@singleton
class MysqlManager(object):
    """docstring for DBManager"""

    def __init__(self, db_host, db_user, db_pass, db_name, db_port=3306):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name
        self.db_port = db_port
        self._add_db()

    def _add_db(self):
        self.db = pymysql.connect(
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            passwd=self.db_pass,
            db=self.db_name,
            charset='utf8mb4')
        self.cursor = self.db.cursor()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor
        except Exception as e:
            print("---rollback--{}".format(e))
            self.db.rollback()
            self._add_db()

    def select(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print("Error")
            return None
