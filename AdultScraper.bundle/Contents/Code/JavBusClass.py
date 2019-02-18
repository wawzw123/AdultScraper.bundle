# -*- coding: utf-8 -*-


class JavBusClass():
    '''
    获取html对象与解析html对象类
    javBusGetHtmlByUrl()获取html对象
    javBusGetInfoByHtml()解析html对象
    '''

    def javBusGetHtmlByUrl(self, url):
        '''
        获取html对象函数
        url:传入站点地址<str>
        return:<dict>
        '''
        Log('开始查询资源执行javBusGetHtmlByUrl函数')
        self.item = {}
        self.item['issuccess'] = False

        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
        try:
            req = requests.get(url, headers=self.headers)
        except requests.exceptions.RequestException, e:
            return self.item
        req.encoding = req.apparent_encoding
        Log('查询数据时站点返回值：%s' % req.status_code)
        if req.status_code == 200:
            html = etree.HTML(req.text)
            self.item['issuccess'] = True
            self.item['html'] = html
            return self.item
        else:
            return self.item

    def javBusGetInfoByHtml(self, html):
        '''
        html对象解析函数
        html:html对象<obj>
        '''

        '初始化字典'
        self.item = {}
        '默认结果成功状态设置为：False'
        self.item['issuccess'] = False
        Log('开始解析html执行javBusGetInfoByHtml函数')
        '初始化部分变量'
        self.item['directors'] = ''
        self.item['collections'] = ''
        
        '单独获取信息部分'

        '海报'
        x_imgurl = html.xpath(
            '//div[@class="col-md-9 screencap"]/a[@class="bigImage"]/@href')
        if not x_imgurl == '':
            self.item["imgurl"] = x_imgurl
        else:
            self.item["imgurl"] = ''

        '标题'
        x_title = html.xpath(
            '//div[@class="col-md-9 screencap"]/a[@class="bigImage"]/img/@title')
        if not x_title == '':
            self.item["title"] = x_title
        else:
            self.item["title"] = ''

        '''
        Begin 类型逻辑处理
        获取演员Div标签备用对比删除使用

        循环字典如果碰到unicode编码:下一个就是值直接取出来
	    uncode对照表
		\u8b58\u5225\u78bc:識別碼
		\u767c\u884c\u65e5\u671f:發行日期
		\u9577\u5ea6：長度
		\u5c0e\u6f14:導演
		\u88fd\u4f5c\u5546:製作商
		\u767c\u884c\u5546:發行商
		\u7cfb\u5217\u003a:系列
        '''
        self.actors_tmp = {}
        self.actors_tmp["actors_tmp"] = html.xpath(
            '//div/p/span[@class="genre"][@onmouseover]/a/text()')
        '获取类型与演员P标签对比删除使用'
        self.type_tmp = {}
        self.type_tmp["type_tmp"] = html.xpath(
            '//div/p/span[@class="genre"]/a/text()')
        for idxt, temp in enumerate(self.type_tmp["type_tmp"]):
            for idxa, temp in enumerate(self.actors_tmp["actors_tmp"]):
                if self.type_tmp["type_tmp"][idxt] == self.actors_tmp["actors_tmp"][idxa]:
                    self.type_tmp["type_tmp"].pop(idxt)
        'End 类型逻辑处理'

        '演员'
        actors_list = html.xpath(
            '//a[@class="avatar-box"]/div[@class="photo-frame"]/img')
        if len(actors_list) > 0:
            t = ''
            for idx, al_element in enumerate(actors_list):
                if (idx+1) < len(actors_list):
                    t += ('%s|%s,' % (al_element.xpath('@title')
                                      [0], al_element.xpath('@src')[0]))
                else:
                    t += ('%s|%s' % (al_element.xpath('@title')
                                     [0], al_element.xpath('@src')[0]))
            self.item.update({"actors": t})
        else:
            self.item['actors'] = ''

        '类别'
        if not self.type_tmp["type_tmp"] == '':
            self.item["type"] = self.type_tmp["type_tmp"]
        else:
            self.item["type"] = ''

        self.info_tmp = {}
        self.info_tmp["info_tmp"] = html.xpath(
            '//div[@class="col-md-3 info"]//text()')

        '番号 id初始化'
        tmp_id = ''
        for idx, temp in enumerate(self.info_tmp["info_tmp"]):
            '番号'
            if self.info_tmp["info_tmp"][idx] == u'\u8b58\u5225\u78bc:':
                tmp_id = self.info_tmp["info_tmp"][idx+2]
                self.item['id'] = tmp_id

            '日期'
            if self.info_tmp["info_tmp"][idx] == u'\u767c\u884c\u65e5\u671f:':
                self.item['originallyAvailableAt'] = self.info_tmp["info_tmp"][idx +
                                                                               1].replace(" ", "")
                self.item['year'] = self.info_tmp["info_tmp"][idx +
                                                              1].replace(" ", "")
            '收藏集'
            
            if self.info_tmp["info_tmp"][idx] == u'\u7cfb\u5217:':
                self.s_tmp = {}
                self.s_tmp['s_tmp'] = html.xpath(
                    '//div[@class="col-md-3 info"]/p/a/text()')
                for idx, temp in enumerate(self.s_tmp['s_tmp']):
                    if (idx+1) == len(self.s_tmp["s_tmp"]):
                        self.item['collections'] = self.s_tmp["s_tmp"][idx]

            '导演'
            if self.info_tmp["info_tmp"][idx] == u'\u5c0e\u6f14:':
                self.item['directors'] = self.info_tmp["info_tmp"][idx+2]

            '演播室'
            if self.info_tmp["info_tmp"][idx] == u'\u88fd\u4f5c\u5546:':
                self.item['studio'] = self.info_tmp["info_tmp"][idx+2]
            

        '介绍'
        Log('开始arzon站点抓取介绍')
        Log('开始确认18获取cookie')
        Url = "https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=https%3A%2F%2Fwww.arzon.jp%2F"
        Log(Url)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
        r = None
        try:
            Log('开始访问介绍arzon站点')
            r = requests.get(Url, headers=headers, allow_redirects=False)
        except requests.exceptions.RequestException, e:
            pass
        if not r == None:
            Log('arzon访问成功带回cookie')
            r.encoding = r.apparent_encoding
            cookie = r.cookies['PHPSESSID']
            Log('开始访问arzon站点获取列表')
            url = 'https://www.arzon.jp/itemlist.html?&q=+{}&t=all&m=all&s=all&d=all&mkt=all&disp=30&sort=-udate&list=list'.format(
                tmp_id)
            Log(url)
            headers = {'Cookie': 'PHPSESSID=%s; __utma=217774537.597254290.1549626845.1549626845.1549626845.1; __utmc=217774537; __utmz=217774537.1549626845.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=217774537.13.10.1549626845' % cookie, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
            req = None
            try:
                req = requests.get(url, headers=headers)
            except requests.exceptions.RequestException, e:
                pass
            if not req == None:
                Log('访问arzon站点带回返回状态')
                req.encoding = req.apparent_encoding
                if req.status_code == 200:
                    Log('状态200站点访问成功')
                    t = req.text
                    t = t.replace(
                        '<?xml version="1.0" encoding="UTF-8"?>', '')
                    t = t.replace(
                        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"', '')
                    t = t.replace(
                        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')
                    html = etree.HTML(t)
                    x_summary = html.xpath('//p[@class="iteminfo"]/text()')
                    Log('x_summary :%s' % x_summary)
                    if len(x_summary) > 0:
                        x_summary = x_summary[0].replace('\r\n', '')
                        self.item['summary'] = x_summary
                    else:
                        self.item['summary'] = ''
                    Log('开始解析html对象')

        self.item['issuccess'] = True
        Log('输出解析html字典')
        Log(self.item)
        return self.item
