# -*-coding:utf-8-*-
from mobpush.model.BasePush import BasePush


class PushMulti(BasePush):
    def __init__(self):
        self.data = {
            "items": [],
            "pushWork": None
        }


class Item(BasePush):
    def __init__(self):
        self.data = {
            "itemId": None,
            "workNo": None,
            "alias": [],
            "rids": [],
            "title": None,
            "content": None
        }
