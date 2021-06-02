import datetime
import sqlite3
import threading
import unittest
import time
import numpy as np
from unittest.case import skip
from queue import Queue
from DATABASE_MANAGER import SQLITE_TOOL



class TEST_DB_MANAGER(unittest.TestCase):
    '''
    測試DB管理模組是否一切正常
    '''
    def setUp(self):
        # lock = threading.Lock
        # self.db_manager = DB_MANAGER("TRADING_DB.db")
        pass

    def test_class_import_successfully(self):
        '''測試模組有成功匯入'''
        sql = SQLITE_TOOL()
        self.assertEqual(sql.filename, "TRADING_DB.db")
        sql.close()

    @skip
    def test_write_into_db(self):
        '''
        測試是否可以成功將資料寫入資料庫
        '''
        try:
            st = time.time()
            sql = SQLITE_TOOL()
            timestamp = list()
            _datetime = list()
            value_1 = list()
            value_2 = list()
            value_3 = list()
            rows = 5000

            info_list = list()
            for _ in range(rows):
                timestamp.append(str(time.time()))
                _datetime.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                value_1.append(str(np.random.rand()))
                value_2.append(str(np.random.rand()))
                value_3.append(str(np.random.rand()))
                info_list.append((timestamp[-1], f'{_datetime[-1]}', value_1[-1], value_2[-1], value_3[-1]))
            ret = False
            try:
                ret = sql.execute(
                    sql='insert into For_test_only values (?,?,?,?,?)', param=info_list
                )
            except:
                time.sleep(1)
                print(f"異常，暫緩一秒再執行")
                ret = sql.execute(
                    sql='insert into For_test_only values (?,?,?,?,?)', param=info_list
                )

            self.assertTrue(ret)
            ed = time.time()
            print(f"插入 {rows} 行資料用了 {ed - st} 秒，平均一行 {(ed-st)/rows} 秒\n")
            print(f"資料庫長度： {len(sql.query('select * from For_test_only;'))}")
            sql.close()
        except Exception as e:
            print(f"test_write_into_db：{e}")
            sql.close()

    @skip
    def test_delete_rows(self):
        '''
        測試是否可以成功將資料從table中刪除
        '''
        sql = SQLITE_TOOL()
        # 先隨便加點東西
        _content = list()
        for i in range(100):
            _content.append([np.random.rand() for _ in range(5)])
        ret = sql.execute(
            sql='insert into For_test_only values (?,?,?,?,?)', param=_content)

        self.assertTrue(ret)
        self.assertTrue(len(sql.query('select * from For_test_only;')) > 0)
        # 確認裡面有東西
        ret = sql.execute('DELETE FROM For_test_only;')
        self.assertTrue(ret)
        self.assertTrue(len(sql.query('select * from For_test_only;')) == 0)
        sql.close()

    @skip
    def test_written_by_thread(self):
        '''
        測試能不能使用多執行緒進行資料寫入
        '''
        def insert_10_rows(t_name, lock):
            lock.acquire()
            sql = SQLITE_TOOL()
            _content = list()
            for i in range(10):
                _content.append((time.time(), f"{t_name}-{i}", 1, 2, 3))
            sql.execute("INSERT INTO For_test_only VALUES (?,?,?,?,?)", _content)
            sql.close()
            lock.release()

        for _ in range(100):
            lock = threading.Lock()
            threading.Thread(target=insert_10_rows, args=(f"THREAD-{_}", lock)).start()

    @skip
    def test_query_by_thread(self):
        '''
        測試能不能使用多執行緒進行資料讀取
        '''
        def read_5_rows(t_name, q):
            sql = SQLITE_TOOL()
            # print(t_name, sql.query("SELECT * FROM Equity LIMIT 5;"))
            
            q.put((f"{t_name}", sql.query("SELECT * FROM Equity LIMIT 5;")))
            sql.close()

        q = Queue()
        _threads = list()

        for _ in range(50):
            # lock = threading.Lock()
            _thread = threading.Thread(target=read_5_rows, args=(f"THREAD-{_}", q))
            _thread.start()
            _threads.append(_thread)
        
        for _ in _threads:
            _.join()
        # 此時所有thread都結束了
        result = list()
        for _ in range(len(_threads)):
            result.append(q.get())
        
        print(result)
        self.assertEqual(len(result), len(_threads))

    def test_thread_in_a_thread_written_data(self):
        '''
        測試能不能在執行緒裡進行另一個執行緒的DB寫入
        '''
        def insert_10_rows_parent(t_name):

            def written_10_rows(t_name, lock):
                lock.acquire()
                sql = SQLITE_TOOL()
                _content = list()
                for i in range(10):
                    _content.append((time.time(), f"{t_name}-{i}", 1, 2, 3))
                sql.execute("INSERT INTO For_test_only VALUES (?,?,?,?,?)", _content)
                sql.close()
                lock.release()
            
            for _ in range(10):
                lock = threading.Lock()
                _t_name = f"{t_name} >> thread-{_}"
                threading.Thread(target=written_10_rows, args=(f"{_t_name}", lock)).start()
                print(f"小緒{_t_name}開始運行")
        
        _threads = list()
        for _ in range(20):
            t_name = f"THREAD.{_}"
            _t = threading.Thread(target=insert_10_rows_parent, args=(t_name,)).start()
            _threads.append(_t)
            print(f"大緒{t_name}開始運行")
        
        for _ in _threads:
            try:
                _.join()
            except Exception as e:
                print(e)
        print(f"執行完畢")


    @skip
    def test_get_data_from_threads(self):
        '''
        測試從多執行緒收取資料
        '''
        pass



    def tearDown(self):
        # sql = SQLITE_TOOL()
        # sql.execute('DELETE FROM For_test_only;')
        # sql.close()
        pass


if __name__ == '__main__':
    unittest.main()