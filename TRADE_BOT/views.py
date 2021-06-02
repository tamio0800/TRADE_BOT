from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


def main_page(request):
    # 首頁
    return HttpResponse("歡迎來到首頁")


def current_status(request):
    # 資訊呈現頁
    return render(request, "current_status.html")
    # return HttpResponse("歡迎來到資訊呈現頁")