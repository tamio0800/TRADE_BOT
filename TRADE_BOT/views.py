from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


def main_page(request):
    # 首頁
    return render(request, "base.html", {"title": "這是首頁"})


def current_status(request):
    # 資訊呈現頁

    context = {
        "title": "交易資訊頁"
    }
    return render(request, "current_status.html", context)
    # return HttpResponse("歡迎來到資訊呈現頁")