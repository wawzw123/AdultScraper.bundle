# -*- coding: utf-8 -*-


class ArzonClass():
    '''
    获取html对象与解析html对象类
    arzonGetHtmlByUrl()获取html对象
    arzonGetInfoByHtml()解析html对象
    '''

    def arzonGetHtmlByUrl(self, url, cookie):
        '''
        获取html对象函数
        url：需要访问的地址<str>
        cookie：站点cookie<str>
        return:<dict>
        '''
        self.item = {}
        self.item['issuccess'] = False
        headers = {'Cookie': 'PHPSESSID=%s; __utma=217774537.597254290.1549626845.1549626845.1549626845.1; __utmc=217774537; __utmz=217774537.1549626845.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=217774537.13.10.1549626845' % cookie, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
        try:
            req = requests.get(url, headers=headers)
        except requests.exceptions.RequestException, e:
            return self.item
        req.encoding = req.apparent_encoding
        if req.status_code == 200:
            t = req.text
            t = t.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            t = t.replace(
                '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"', '')
            t = t.replace(
                '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')
            html = etree.HTML(t)
            self.item['issuccess'] = True
            self.item['html'] = html
            return self.item
        else:
            return self.item

    def arzonGetInfoByHtml(self, html):
        '''
        html对象解析函数
        html:html对象<obj>
        '''
        self.item['issuccess'] = False
        self.item_list = []

        for idx, item in enumerate(html.xpath('//div[@id="item"]/div[@class="pictlist"]/dl/dd[@class="entry-title"]/h2/a/@href')):
            '开始循环解析'
            self.item = {}
            '''
            初始化字典

            获取cookie
            '''
            Url = "https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=https%3A%2F%2Fwww.arzon.jp%2F"
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
            try:
                r = requests.get(Url, headers=headers, allow_redirects=False)
            except requests.exceptions.RequestException, e:
                return self.item
            r.encoding = r.apparent_encoding
            cookie = r.cookies['PHPSESSID']

            '开始解析html页面'
            url = 'https://www.arzon.jp{}'.format(item)
            headers = {'Cookie': 'PHPSESSID=%s; __utma=217774537.597254290.1549626845.1549626845.1549626845.1; __utmc=217774537; __utmz=217774537.1549626845.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=217774537.13.10.1549626845' % cookie, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
            try:
                req = requests.get(url, headers=headers)
            except requests.exceptions.RequestException, e:
                return self.item
            req.encoding = req.apparent_encoding
            if req.status_code == 200:
                t = req.text
                t = t.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
                t = t.replace(
                    '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"', '')
                t = t.replace(
                    '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', '')
                html = etree.HTML(t)
                '开始写入字典'

                '番号'
                x_id = html.xpath('/html/body[@id="layout3"]/div[@id="container"]/div[@id="contentsArea"]/div[@id="containerArea"]/div[@id="contents"]/div[@id="main"]/div[@class="mainInner innerDetail"]/div[@id="detail_new"]/table//tr/td[1]/table[@class="item_detail"]//tr[3]/td[@class="text"]/div[@class="item_register"]/table[@class="item"]//tr[8]/td[2]/text()')
                if len(x_id) > 0:
                    self.item['id'] = x_id[0].replace('\r\n', '').replace(
                        ' ', '').replace(u'\xa0\xa0\u5ec3\u76e4', '')
                else:
                    self.item['id'] = ''
                Log(x_id)

                '标题'
                x_title = html.xpath(
                    '//div[@class="detail_title_new2"]/table/tr/td/h1/text()')[0]
                if not x_title == '':
                    self.item['title'] = x_title
                else:
                    self.item['title'] = ''
                Log(x_title)

                '海报'
                x_imgurl = self.item["imgurl"] = html.xpath(
                    '//table//tr//td//a[@data-lightbox="jacket2"]/@href')
                if len(x_imgurl) > 0:
                    self.item['imgurl'] = 'https:%s' % x_imgurl[0]
                else:
                    self.item['imgurl'] = ''
                Log(x_imgurl)

                '日期'
                self.item['originallyAvailableAt'] = ''
                self.item['year'] = ''

                '介绍'
                x_summary = self.item['summary'] = html.xpath(
                    '/html/body[@id="layout3"]/div[@id="container"]/div[@id="contentsArea"]/div[@id="containerArea"]/div[@id="contents"]/div[@id="main"]/div[@class="mainInner innerDetail"]/div[@id="detail_new"]/table//tr/td[1]/table[@class="item_detail"]//tr[2]/td[@class="text"]/div[@class="item_text"]/text()')
                if len(x_summary) > 0:
                    self.item['summary'] = x_summary[1].replace(
                        '\r\n', '').replace(' ', '')
                else:
                    self.item['summary'] = ''                
                Log(x_summary)

                '收藏集'
                x_collections = html.xpath(
                    '/html/body[@id="layout3"]/div[@id="container"]/div[@id="contentsArea"]/div[@id="containerArea"]/div[@id="contents"]/div[@id="main"]/div[@class="mainInner innerDetail"]/div[@id="detail_new"]/table//tr/td[1]/table[@class="item_detail"]//tr[3]/td[@class="text"]/div[@class="item_register"]/table[@class="item"]//tr[4]/td[2]/a/text()')
                if len(x_collections) > 0:
                    self.item['collections'] = x_collections[0]
                else:
                    self.item['collections'] = ''             
                Log(x_collections)

                '导演'
                x_directors = html.xpath(
                    '/html/body[@id="layout3"]/div[@id="container"]/div[@id="contentsArea"]/div[@id="containerArea"]/div[@id="contents"]/div[@id="main"]/div[@class="mainInner innerDetail"]/div[@id="detail_new"]/table//tr/td[1]/table[@class="item_detail"]//tr[3]/td[@class="text"]/div[@class="item_register"]/table[@class="item"]//tr[5]/td[2]/a/text()')
                if len(x_directors) > 0:
                    self.item['directors'] = x_directors[0]
                else:
                    self.item['directors'] = ''        
                Log(x_directors)

                '演播室'
                x_studio = html.xpath(
                    '/html/body[@id="layout3"]/div[@id="container"]/div[@id="contentsArea"]/div[@id="containerArea"]/div[@id="contents"]/div[@id="main"]/div[@class="mainInner innerDetail"]/div[@id="detail_new"]/table//tr/td[1]/table[@class="item_detail"]//tr[3]/td[@class="text"]/div[@class="item_register"]/table[@class="item"]//tr[2]/td[2]/a/text()')
                if len(x_studio) > 0:
                    self.item['studio'] = x_studio[0]
                else:
                    self.item['studio'] = ''      
                Log(x_studio)

                '演员'
                t = ''
                actors_list = html.xpath(
                    '/html/body[@id="layout3"]/div[@id="container"]/div[@id="contentsArea"]/div[@id="containerArea"]/div[@id="contents"]/div[@id="main"]/div[@class="mainInner innerDetail"]/div[@id="detail_new"]/table//tr/td[1]/table[@class="item_detail"]//tr[3]/td[@class="text"]/div[@class="item_register"]/table[@class="item"]//tr[1]/td[2]/a/text()')
                if len(actors_list) > 0:
                    for idx, temp in enumerate(actors_list):
                        if (idx+1) < len(actors_list):
                            t += ('%s,' % temp)
                        else:
                            t += ('%s' % temp)
                        self.item.update({"actors": t})
                else:
                    self.item['actors'] = ''

                '类别'
                t = ''
                type_list = html.xpath(
                    '//div[@id="adultgenre2"]//table//tr//td//ul/li/a/text()')
                if len(type_list) > 0:
                    for idx, temp in enumerate(type_list):
                        if (idx+1) < len(type_list):
                            t += ('%s,' % temp)
                        else:
                            t += ('%s' % temp)
                        self.item.update({"type": t})
                else:
                    self.item['type'] = ''
            self.item['issuccess'] = True
            self.item_list.append(self.item)
        return self.item_list
