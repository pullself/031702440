# -*- coding:utf-8 -*-
import re


class people_info:
    def __init__(self):
        self.name = None
        self.tel = None
        self.addr = []

    def set_name(self, ad):
        ret = re.search(r"(.+),(.*)", ad)
        # print(ret.group())
        self.name = ret.group(1)
        return ret.group(2)

    def set_tel(self, ad):
        ret = re.search(r"\d{11}", ad)
        # print(ret.group())
        self.tel = ret.group()
        return ad.replace(ret.group(), '')

    def cut_addr(self, ad):
        pass

    def set_addr(self, ad, lv):
        pass

    def deal(self, ad):
        pass

    def get_name(self):
        return self.name

    def get_tel(self):
        return self.tel

    def get_addr(self):
        return self.addr


if __name__ == "__main__":
    pass
