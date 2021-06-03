from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .DATABASE_MANAGER import SQLITE_TOOL
import os


def main_page(request):
    # 首頁
    return render(request, "base.html", {"title": "這是首頁"})


def current_status(request):
    # 資訊呈現頁
    print(os.listdir())
    sql = SQLITE_TOOL(filename='trading_dbs/TRADING_DB.db')
    result = sql.query('select * from Equity order by timestamp desc limit 15;')
    sql.close()

    info = list()
    # info = {
    #     "datetime": list(),
    #     "equity": list(),
    #     "free_equity": list(),
    #     "unrealized_profit": list(),
    #     "unrealized_loss": list(),
    # }  # 要餵給templates的context參數之一

    for _ in result:
        info.append((
            _[1], _[2], _[3], _[9], _[10]
        ))
        # info["datetime"].append(_[1])
        # info["equity"].append(_[2])
        # info["free_equity"].append(_[3])
        # info["unrealized_profit"].append(_[9])
        # info["unrealized_loss"].append(_[10])

    context = {
        "title": "交易資訊頁",
        "info": info
    }
    return render(request, "current_status.html", context)
    # return HttpResponse("歡迎來到資訊呈現頁")