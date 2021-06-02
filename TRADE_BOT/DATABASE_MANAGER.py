import sqlite3
import threading
import multiprocessing
import time
import os
import pandas as pd
import datetime
# from PROGENERAL_FUNCTIONS import timestamp_to_datetime_str

class SQLITE_TOOL():
    """
    simpleToolSql for sqlite3
    简单数据库工具类
    编写这个类主要是为了封装sqlite，继承此类复用方法
    """

    def __init__(self, filename="DB_APP/TRADING_DB.db", thread_lock=False):
        """
        初始化数据库，默认文件名 stsql.db
        filename：文件名
        """
        self.filename = filename
        if thread_lock != False:
            self.lock = thread_lock
            self.lock.acquire()
        else:
            self.lock = False
        self.db = sqlite3.connect(self.filename, timeout=60)
        self.c = self.db.cursor()
        
    def close(self):
        """
        关闭数据库
        """
        self.c.close()
        self.db.close()
        if self.lock != False:
            self.lock.release()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.c.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else :
                    self.c.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            return False, e
        if count > 0 :
            return True
        else :
            return False

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        if param is None:
            self.c.execute(sql)
        else:
            self.c.execute(sql, param)
        return self.c.fetchall()
        


if __name__ == '__main__':
    pass


    # group_result = \
    #     sql.query('SELECT symbol, direction, SUM(order_size) \
    #         FROM Orders_test WHERE symbol = \"NEO/USDT\" GROUP BY direction;')
    # for _ in group_result:
    #     print(_)
    # sql.execute("INSERT INTO For_test_only VALUES (?,?,?,?)", (1500.13, "hihi", "1500.13", 100))

    # def written_for_test(t_name, db_name, lock):
    #     lock.acquire()
    #     sql = SQLITE_TOOL(db_name)
    #     for _ in range(3):
    #         sql.execute("INSERT INTO For_test_only VALUES (?,?,?,?)", (1500.13, f"{t_name}-{_}", "1500.13", 100))
    #     sql.close()
    #     lock.release()

    # threads = list()
    # for _ in range(44):
    #     if _ < 34:
    #         db_name = 'TRADING_DB'
    #     else:
    #         db_name = 'MEAN_REVERSE_30M'
    #     lock = threading.Lock()
    #     _ = str(_).rjust(2, '0')
    #     threads.append(threading.Thread(target=written_for_test, args=(f"thread_{_}",db_name,lock)))
    
    # def run_thread(_ts):
    #     for _ in _ts:
    #         _.start()
    #     for _ in _ts:
    #         _.join()

    # multiprocessing.Process(target=run_thread, args=(threads[:34],)).start()
    # multiprocessing.Process(target=run_thread, args=(threads[34:],)).start()

    # df = pd.read_csv("../logs/BINANCE_EQUITY_LOGS.csv")
    # df.loc[:, 'timestamp'] = df.Datetime.apply(pd.to_datetime).apply(datetime.datetime.timestamp)
    # print(df.tail())
    
    # sql = SQLITE_TOOL()

    # _list = list()
    # for i in range(df.shape[0]):
    #     _list.append(
    #         (
    #             df.loc[i].timestamp, df.loc[i].Datetime, df.loc[i].Equity, df.loc[i].Free_Equity, df.loc[i].Used_Equity,
    #             int(df.loc[i].Long_Counts), int(df.loc[i].Short_Counts), 
    #             int(df.loc[i].Posistions_With_Profit), int(df.loc[i].Posistions_With_Loss), 
    #             df.loc[i].Unrealized_Profit, df.loc[i].Unrealized_Loss
    #         )
    #     )
    # sql.execute('INSERT INTO Equity VALUES (?,?,?,?,?,?,?,?,?,?,?)', _list)
    # sql.close()