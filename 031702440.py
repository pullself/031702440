# coding=utf-8
import re
import json
from urllib import request, parse

province = u"(河北|山西|辽宁|吉林|黑龙江|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|海南|四川|贵州|云南|陕西|甘肃|青海|台湾|内蒙古|广西|西藏|宁夏|新疆|香港|澳门)"
city1 = u"(石家庄|唐山|秦皇岛|邯郸|邢台|保定|张家口|承德|沧州|廊坊|衡水|太原|大同|阳泉|长治|晋城|朔州|晋中|运城|忻州|临汾|吕梁|呼和浩特|包头|乌海|赤峰|通辽|鄂尔多斯|呼伦贝尔|巴彦淖尔|乌兰察布|沈阳|大连|鞍山|抚顺|本溪|丹东|锦州|营口|阜新|辽阳|盘锦|铁岭|朝阳|葫芦岛|"
city2 = u"长春|吉林|四平|辽源|通化|白山|白城|松原|哈尔滨|齐齐哈尔|牡丹江|佳木斯|大庆|伊春|鸡西|鹤岗|双鸭山|七台河|绥化|黑河|南京|无锡|徐州|常州|苏州|南通|宿迁|淮安|盐城|扬州|镇江|泰州|连云港|"
city3 = u"杭州|宁波|温州|绍兴|湖州|嘉兴|金华|衢州|台州|丽水|舟山|合肥|芜湖|蚌埠|淮南|马鞍山|淮北|铜陵|安庆|黄山|阜阳|宿州|滁州|六安|宣城|池州|亳州|福州|莆田|泉州|厦门|漳州|龙岩|三明|南平|宁德|"
city4 = u"南昌|赣州|宜春|吉安|上饶|抚州|九江|景德镇|萍乡|新余|鹰潭|济南|青岛|淄博|枣庄|东营|烟台|潍坊|济宁|泰安|威海|日照|滨州|德州|聊城|临沂|菏泽|郑州|开封|洛阳|平顶山|安阳|鹤壁|新乡|焦作|濮阳|许昌|漯河|三门峡|商丘|周口|驻马店|南阳|信阳|"
city5 = u"武汉|黄石|十堰|荆州|宜昌|襄阳|鄂州|荆门|黄冈|孝感|咸宁|随州|长沙|株洲|湘潭|衡阳|邵阳|岳阳|张家界|益阳|常德|娄底|郴州|永州|怀化|"
city6 = u"广州|深圳|珠海|汕头|佛山|韶关|湛江|肇庆|江门|茂名|惠州|梅州|汕尾|河源|阳江|清远|东莞|中山|潮州|揭阳|云浮|海口|三亚|三沙|儋州|"
city7 = u"成都|绵阳|自贡|攀枝花|泸州|德阳|广元|遂宁|内江|乐山|资阳|宜宾|南充|达州|雅安|眉山|巴中|广安|贵阳|遵义|安顺|铜仁|毕节|六盘水|昆明|昭通|曲靖|玉溪|普洱|保山|丽江|临沧|"
city8 = u"拉萨|昌都|山南|日喀则|那曲|林芝|西安|铜川|宝鸡|咸阳|渭南|汉中|安康|商洛|延安|榆林|兰州|嘉峪关|金昌|白银|天水|酒泉|张掖|武威|定西|陇南|平凉|庆阳|"
city9 = u"西宁|海东|银川|石嘴山|吴忠|固原|中卫|乌鲁木齐|克拉玛依|吐鲁番|哈密)"

judge = ['县','区','街道','镇','乡','路','道','街','巷']

class PeopleInfo:
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
        ret = re.search("(北京|上海|天津|重庆)([市]?)((.{1,4}?区|[^0-9]{1,4}?县|.{1,4}?市)?)((.{1,4}?街道|.{1,4}?镇|.{1,4}?乡)?)((.{1,6}?路|.{1,6}?街|.{1,6}?巷|.{1,6}?弄|.{1,6}?道)?)((\d+?号)?)(.*)",
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
        ret = re.search("([^0-9]+?省|.+?自治区)(.{1,4}?市|.{4,8}?自治州|.{2,4}?地区|.{2,4}?盟)((.{1,4}?区|[^0-9]{1,4}?县|.{1,4}?市|.{2,6}?旗)?)((.{1,4}?街道|.{1,4}?镇|.{1,4}?乡)?)((.{1,6}?弄|.{1,6}?路|.{1,6}?街|.{1,6}?巷|.{1,6}?道)?)((\d+?号)?)(.*)",
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
        ret = re.search("("+province+ "?)" + "([省]?)" + "(" + city1 + city2 + city3 + city4 + city5 + city6 + city7 + city8 + city9 + "?)" + r"([市]?)((.{0,4}?区|[^0-9]{0,4}?县|.{0,4}?市)?)((.{0,4}?街道|.{0,4}?镇|.{0,4}?乡)?)((.{0,6}?路|.{0,6}?街|.{0,6}?巷|.{0,6}?道)?)((\d+?号)?)(.*)",
            ad)
        if (ret):
            if (ret.group(1) != ''):
                if(ret.group(1)=='香港' or ret.group(1) == '澳门'):
                    self.__addr.append(ret.group(1) + '特别行政区')
                elif(ret.group(1)=='内蒙古' or ret.group(1)=='西藏'):
                    self.__addr.append(ret.group(1)+'自治区')
                elif(ret.group(1)=='广西'):
                    self.__addr.append(ret.group(1)+'壮族自治区')
                elif(ret.group(1)=='宁夏'):
                    self.__addr.append(ret.group(1)+'回族自治区')
                elif(ret.group(1)=='新疆'):
                    self.__addr.append(ret.group(1)+'维吾尔自治区')
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
            data = []
            url = "https://restapi.amap.com/v3/place/text?"+"keywords="+parse.quote(ad.rstrip('.'))+"&output=json&offset=1&key=fb4598362a6784eaaf006e6e07a66f4a&extensions=all"
            res = request.urlopen(url)
            res = json.loads(res.read().decode('utf-8'))
            url = "https://restapi.amap.com/v3/geocode/regeo?output=json&location={}&key=fb4598362a6784eaaf006e6e07a66f4a&extensions=all".format(res['pois'][0]['location'])
            res = request.urlopen(url)
            res = json.loads(res.read().decode('utf-8'))
            data.append(res['regeocode']['addressComponent']['province'])
            if(data[0]=='北京市' or data[0]=='上海市' or data[0]=='天津市' or data[0]=='重庆市'):
                data[0] = data[0].strip('市')
            if(res['regeocode']['addressComponent']['city']==[]):
                data.append('')
            else:
                data.append(res['regeocode']['addressComponent']['city'])
            data.append(res['regeocode']['addressComponent']['district'])
            data.append(res['regeocode']['addressComponent']['township'])
            data.append(res['regeocode']['addressComponent']['streetNumber']['street'])
            data.append(res['regeocode']['addressComponent']['streetNumber']['number'])
            data.append(res['regeocode']['addressComponent']['building']['name'])
            for i in range(7):
                if (self.__addr[i] == ''):
                    if (data[i] != ''):
                        self.__addr[i] = data[i]
        return self.__addr

    def get_name(self):
        return self.__name

    def get_tel(self):
        return self.__tel

    def get_addr(self):
        return self.__addr

x = input()
dic = {}
t = PeopleInfo()
t.deal(x)
dic.update({'姓名': t.get_name()})
dic.update({'手机': t.get_tel()})
dic.update({'地址': t.get_addr()})
js = json.dumps(dic,ensure_ascii=False)
print(js)