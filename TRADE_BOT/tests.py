from unittest.case import skip
from django.test import TestCase, Client
from datetime import datetime
from .DATABASE_MANAGER import SQLITE_TOOL


class SHOW_INFO(TestCase):
    '''
    用來確認最基本的資訊是否能正常顯示
    '''
    def setUp(self):
        self.client = Client()

    def test_has_main_url(self):
        # 確認主頁的url存在
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # print(response.content.decode("utf8"))
    
    def test_has_information_url(self):
        # 確認show出資訊的url存在
        response = self.client.get('/current_status/')
        self.assertEqual(response.status_code, 200)

    @skip
    def test_show_equity(self):
        # 確認可以讀取資料庫內的資訊，並顯示在網頁上
        response = self.client.get('/current_status/')
        self.assertIn("保證金餘額(USDT)", response.content.decode("utf8"))
        self.assertIn("9897", response.content.decode("utf8"))
