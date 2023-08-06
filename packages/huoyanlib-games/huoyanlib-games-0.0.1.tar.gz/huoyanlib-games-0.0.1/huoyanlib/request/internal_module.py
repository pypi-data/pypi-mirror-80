import requests
import bs4
import urllib
import sys
import re
from huoyanlib.request import _raise_huoyanlibrequesterror_sys
from socket import*


def get_user_cookies():
    try:
        new = sys.argv[1]
        new = new.replace(';', ' ')
        new = new.split()
        result = new[4]
        result = result.replace('stu_id=', ' ')
        result = result.strip()
        return int(result)
    except IndexError:
        _raise_huoyanlibrequesterror_sys()


def login(user, password):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(("pan.asunc.cn", 22001))
        s.send(user.encode("utf-8"))
        s.send(password.encode("utf-8"))
        print(s.recv(1).decode("utf-8"))
    except:
        raise Exception("连接服务器失败")
