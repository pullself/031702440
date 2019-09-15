# -*- coding:utf-8 -*-
import re
import json
from urllib import request, parse
from base import province, city1, city2, city3, city4, city5, city6, city7, city8, city9

addresslv = ['province', 'city', 'district', 'town', 'street']
judge = ['县','区','街道','镇','乡','路','道','街','巷']


class People_info:
    def __init__(self):
        self.__addr = []
        self.__name = ''
        self.__tel = ''
    
    def deal(self,ad):
        lv = ad[0]
        ad = ad[2:]
        # print(ad)
        try:
            ad = self.set_name(ad)
        except AttributeError:
            print("'" + ad + "'" + ":姓名输入格式不符合规范")
        try:
            ad = self.set_tel(ad)
        except AttributeError:
            print("'" + ad + "'" + ":手机输入格式不符合规范")
        try:
            self.set_addr(ad, int(lv))
        except AttributeError:
            print("'" + ad + "'" + ":地址输入格式不符合规范")
        return self.__addr

    def set_name(self, ad):
        ret = re.search(r"(.+),(.*)", ad)
        # print(ret.group())
        self.__name = ret.group(1)
        return ret.group(2)

    def set_tel(self, ad):
        ret = re.search(r"\d{11}", ad)
        # print(ret.group())
        self.__tel = ret.group()
        ad = ad.rstrip('\n')
        return ad.replace(ret.group(), '')

    def cut_addr(self, ad):
        ret = re.search(r"(北京|上海|天津|重庆)([市]?)((.{1,4}?区|[^0-9]{1,4}?县|.{1,4}?市)?)((.{1,4}?街道|.{1,4}?镇|.{1,4}?乡)?)((.{1,6}?路|.{1,6}?街|.{1,6}?巷|.{1,6}?弄|.{1,6}?道)?)((\d+?号)?)(.*)",
            ad)
        if (ret):
            self.__addr.append(ret.group(1))
            self.__addr.append(ret.group(1) + '市')
            i = 3
            while (i < 11):
                self.__addr.append(ret.group(i))
                i += 2
            self.__addr.append(ret.group(11).rstrip('.'))
            return self.__addr
        ret = re.search(r"([^0-9]+?省|.+?自治区)(.{1,4}?市)((.{1,4}?区|[^0-9]{1,4}?县|.{1,4}?市)?)((.{1,4}?街道|.{1,4}?镇|.{1,4}?乡)?)((.{1,6}?弄|.{1,6}?路|.{1,6}?街|.{1,6}?巷|.{1,6}?道)?)((\d+?号)?)(.*)",
            ad)
        if (ret):
            self.__addr.append(ret.group(1))
            self.__addr.append(ret.group(2))
            i = 3
            while (i < 11):
                self.__addr.append(ret.group(i))
                i += 2
            self.__addr.append(ret.group(11).rstrip('.'))
            return self.__addr
        ret = re.search(r"("+province+ r"?)" + r"([省]?)" + r"(" + city1 + city2 + city3 + city4 + city5 + city6 + city7 + city8 + city9 + r"?)" + r"([市]?)((.{0,4}?区|[^0-9]{0,4}?县|.{0,4}?市)?)((.{0,4}?街道|.{0,4}?镇|.{0,4}?乡)?)((.{0,6}?路|.{0,6}?街|.{0,6}?巷|.{0,6}?道)?)((\d+?号)?)(.*)",
            ad)
        if (ret):
            if (ret.group(1) != ''):
                if(ret.group(1)=='香港' or ret.group(1) == '澳门'):
                    self.__addr.append(ret.group(1) + '特别行政区')
                else:
                    self.__addr.append(ret.group(1) + '省')
            else:
                self.__addr.append(ret.group(1))
            if (ret.group(4) != ''):
                self.__addr.append(ret.group(4) + '市')
            else:
                self.__addr.append(ret.group(4))
            i = 7
            while (i < 15):
                # print(ret.group(i))
                if ret.group(i) in judge:
                    self.__addr.append(self.__addr[1].replace('市',ret.group(i)))
                    self.__addr[1] = ''
                else:
                    self.__addr.append(ret.group(i))
                i += 2
            self.__addr.append(ret.group(15).rstrip('.'))
            # print(self.__addr)
            return self.__addr

    def set_addr(self, ad, lv):
        self.cut_addr(ad)
        if (lv == 1):
            s = self.__addr[4] + self.__addr[5] + self.__addr[6]
            self.__addr = self.__addr[:4]
            self.__addr.append(s)
        elif (lv == 3):
            ret = re.search(r"\d+?号", ad)
            if (ret):
                ad = ad.replace(ret.group(0), '')
            url = 'http://api.map.baidu.com/place/v2/search?' + 'query=' + parse.quote(ad.rstrip('.')) + '&region=' + parse.quote('全国') + '&ak=hrbEuMUarmqy4EFtskzLpl0OgbOjZRGv&output=json'
            res = request.urlopen(url)
            res = json.loads(res.read().decode('utf-8'))
            # print(res)
            lat = res['results'][0]['location']['lat']
            lng = res['results'][0]['location']['lng']
            url = 'http://api.map.baidu.com/reverse_geocoding/v3/?location={},{}&ak=hrbEuMUarmqy4EFtskzLpl0OgbOjZRGv&output=json'.format(lat, lng)
            res = request.urlopen(url)
            res = json.loads(res.read().decode('utf-8'))
            for i in range(5):
                if (self.__addr[i] == ''):
                    if (res['result']['addressComponent'][addresslv[i]] != ''):
                        self.__addr[i] = res['result']['addressComponent'][addresslv[i]]
            # print(res)
        return self.__addr

    def get_name(self):
        return self.__name

    def get_tel(self):
        return self.__tel

    def get_addr(self):
        return self.__addr


if __name__ == "__main__":
    js = []
    ms = open('input.txt', 'r')
    for line in ms.readlines():
        dic = {}
        t = People_info()
        t.deal(line)
        # s = "1!小陈,广东省东莞市凤岗13965231525镇凤平路13号."
        dic.update({'姓名': t.get_name()})
        dic.update({'手机': t.get_tel()})
        dic.update({'地址': t.get_addr()})
        js.append(dic)
    with open('output.json', 'w', encoding='utf-8') as f:
        output = json.dump(js, f, ensure_ascii=False)
