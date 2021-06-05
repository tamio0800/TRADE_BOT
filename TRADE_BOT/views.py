from re import L
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

    def format_val(target):
        _target = float(target)
        if _target == 0:
            return ""
        else:
            _target = f"{int(round(_target)):,}"
            if _target[0] == "-":
                _target = f"- {_target[1:]}"
            return _target
    
    sql = SQLITE_TOOL(filename='trading_dbs/TRADING_DB.db')
    equity_result = sql.query('select * from Equity order by timestamp desc limit 15;')
    sql.close()

    sql = SQLITE_TOOL(filename='trading_dbs/YUTING_30M.db')
    operating_result = sql.query('select * from Logs order by timestamp desc limit 50;')
    sql.close()

    equity_info = list()  # 回傳績效資訊
    operating_logs = list()  # 回傳運作的紀錄

    for _ in equity_result:
        _datatime = _[1][:-3]
        _equity = format_val(_[2])
        _free_equity = format_val(_[3])
        _unrealized_profit = f"+ {format_val(_[9])}" if format_val(_[9]) != "" else ""
        _unrealized_loss = format_val(_[10])

        equity_info.append((
            _datatime, _equity, _free_equity, _unrealized_profit, _unrealized_loss
        ))
    
    if len(operating_result) == 0:
        # 沒有資料
        operating_logs.append(("", ""))
    else:
        for _ in operating_result:
            print(f"_ {_}")
            _datatime = _[1][:-3]
            _statement = _[2].strip()
            operating_logs.append((_datatime, _statement))
    
    print(f"operating_logs {operating_logs}")


    context = {
        "title": "模型概況",
        "equity_info": equity_info,
        "operating_logs": operating_logs
    }
    return render(request, "current_status.html", context)
    # return HttpResponse("歡迎來到資訊呈現頁")