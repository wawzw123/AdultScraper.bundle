# -*- coding: utf-8 -*-

import re
import urllib2
import json
import ssl
import os
import requests
import httplib
import md5
import urllib
import random

from io import BytesIO
from PIL import Image

from datetime import datetime
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from lxml import etree

from JavBusClass import JavBusClass
from ArzonClass import ArzonClass


def Start():
    'Start为 plex plug-in运行的必要函数直接pass即可'
    pass


class AdultScraperAgent(Agent.Movies):
    '''
    Prefs['']:获取Contents/的DefaultPrefs.js中的变量
    '''
    name = u'AdultScraper'
    languages = [Locale.Language.English]
    primary_provider = True
    '辅助代理'
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang, manual):
        '''
        重写查询函数：
        lang:语言<str>
        来源于修正匹配->搜索选项中的语言选择字段
        media：基本信息<obj>.<str>
        来源于修正匹配->搜索选项中的语言选择字段
        在search函数中只传递了两个值：media.name与media.year
        manual:手动模式 <bool>
        来源于修正匹配->搜索选项中选择Avgua点击搜索时
        来源于更多->刷新数据源时(已经手动匹配过一次后否则按照原有执行如自动搜刮或不执行)
        '''
        if Prefs['Is_jp']:
            '判断是否启用javbus数据源'
            Log('选择了使用日本数据源')
            query = media.name.replace(' ', '-')  # 获取文件名
            if manual:
                Log('选择了日本数据源【手动模式】')
                Log('开始18确认带回cookie')
                Url = "https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=https%3A%2F%2Fwww.arzon.jp%2F"
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
                try:
                    r = requests.get(Url, headers=headers,
                                     allow_redirects=False)
                except requests.exceptions.RequestException, e:
                    Log('发生异常:%s' % e)
                    return
                r.encoding = r.apparent_encoding
                cookie = r.cookies['PHPSESSID']
                Log('带回cookie成功')
                url = 'https://www.arzon.jp/itemlist.html?t=&m=all&s=&q={}'.format(
                    query)
                Log('开始获取获取html对象')
                clas_s = ArzonClass()
                clas_s_item = clas_s.arzonGetHtmlByUrl(url, cookie)
                if clas_s_item['issuccess']:
                    Log('获取html对象成功')
                    Log('开始解析html对象')
                    clas_s_data = clas_s.arzonGetInfoByHtml(
                        clas_s_item['html'][0])
                    for i, item in enumerate(clas_s_data):
                        Log('开始循环获取结果')
                        if item['issuccess']:
                            Log(item)
                            id = '{}:{}:{}'.format(
                                item['id'], 'M', i)
                            name = '{} {}'.format(
                                item['id'], item['title'])
                            Log(name)
                            score = 100
                            new_result = dict(
                                id=id, name=name, year='', score=score, lang=lang)
                            Log(new_result)
                            results.Append(
                                MetadataSearchResult(**new_result))
            else:
                Log('选择了日本数据源【自动模式】')
                url = 'https://www.javbus.com/%s' % query
                clas_s = JavBusClass()
                clas_s_item = clas_s.javBusGetHtmlByUrl(url)
                if clas_s_item['issuccess']:
                    clas_s_data = clas_s.javBusGetInfoByHtml(
                        clas_s_item['html'][0])
                    if clas_s_data['issuccess']:
                        id = '{}:{}'.format(clas_s_data['id'], 'A')
                        name = '{} {}'.format(
                            clas_s_data['id'], clas_s_data['title'][0])
                        score = 100
                        new_result = dict(
                            id=id, name=name, year='', score=score, lang=lang)
                        Log(new_result)
                        results.Append(MetadataSearchResult(**new_result))

    def update(self, metadata, media, lang):
        '''
        重写更新函数
        metadata：影片详细信息执行修改<obj>.<str>(具体看api)
        media：影片基本信息<obj>.<str>(具体看api)
        lang：语言
        '''
        vids = metadata.id.split(':')
        Log(vids)
        vid = vids[0]
        '''
        番号
        查询时选定目录列表带过来的id在search函数下手动或自动if clas_s_data["issuccess"]附近
        '''
        vid_M = vids[1]
        '''
        手动模式 OR 自动模式
        查询时选定目录列表带过来的id在search函数下手动或自动if clas_s_data["issuccess"]附近
        '''
        vid_i = None
        if vid_M == 'M':
            vid_i = int(vids[2])
            '''
            执行serch函数时手动模式下选择目录列表序列index（选择当前行的序列号）
            查询时选定目录列表带过来的id在search函数下手动或自动if clas_s_data["issuccess"]附近
            '''
        url = ''
        clas_s_item = {}
        '获取html对象使用'
        clas_s_data = {}
        '解析html对象后使用'
        clas_s_data_list = ''
        '解析多个html对象后使用'
        if Prefs['Is_jp']:
            '''
            判断是否使用javbus数据源并且开始执行获取html对象
            '''
            if vid_M == 'M':
                '判断是否使用了手动搜刮模式'

                '获取arzon站点18确认带回cookie值'
                getcookieUrl = "https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=https%3A%2F%2Fwww.arzon.jp%2F"
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'utf-8', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
                r = None
                try:
                    r = requests.get(
                        getcookieUrl, headers=headers, allow_redirects=False)
                except requests.exceptions.RequestException, e:
                    pass
                if not r == None:
                    r.encoding = r.apparent_encoding
                    cookie = r.cookies['PHPSESSID']

                    '开始获取aron站点查询结果页面'
                    url = 'https://www.arzon.jp/itemlist.html?t=&m=all&s=&q=%s' % vid
                    Log(url)
                    clas_s = ArzonClass()
                    clas_s_item = clas_s.arzonGetHtmlByUrl(url, cookie)

            elif vid_M == 'A':
                '判断是否使用自动搜刮模式'
                url = 'https://www.javbus.com/%s' % vid
                Log(url)
                clas_s = JavBusClass()
                clas_s_item = clas_s.javBusGetHtmlByUrl(url)

        if clas_s_item['issuccess']:
            '判断获取html对象是否数据返回成功<bool>'
            if Prefs['Is_jp']:
                '判断是否使用了使用javbus数据源'
                if vid_M == 'M':
                    '判断是否手动搜刮模式arzon数据源，并且开始解析html对象'
                    clas_s_data_list = clas_s.arzonGetInfoByHtml(
                        clas_s_item['html'][0])
                    clas_s_data = clas_s_data_list[vid_i]
                if vid_M == 'A':
                    '判断是否自动搜刮模式javbus数据源，并且开始解析html对象'
                    clas_s_data = clas_s.javBusGetInfoByHtml(
                        clas_s_item['html'][0])
            if clas_s_data['issuccess']:
                '''
                判断解析html是否成功<bool>

                开始写入plex库
                '''

                '标题'
                name = ''
                if Prefs['Is_jp']:
                    if Prefs['Title_jp'] == '番号':
                        name = '{}'.format(clas_s_data['id'])
                    elif Prefs['Title_jp'] == '标题':
                        name = '{}'.format(clas_s_data['title'][0])
                    elif Prefs['Title_jp'] == '番号,标题':
                        name = '{} {}'.format(
                            clas_s_data['id'], clas_s_data['title'][0])
                metadata.title = name

                '介绍'
                Log(clas_s_data['summary'])
                if not clas_s_data['summary'] == '':
                    metadata.summary = '{}'.format(clas_s_data['summary'])
                '日期'
                if not clas_s_data['originallyAvailableAt'] == '':
                    date_object = datetime.strptime(
                        clas_s_data['originallyAvailableAt'], '%Y-%m-%d')
                    metadata.originally_available_at = date_object
                    metadata.year = metadata.originally_available_at.year
                    Log(metadata.originally_available_at)
                '演播室'
                if not clas_s_data['studio'] == '':
                    metadata.studio = '{}'.format(clas_s_data['studio'])
                '导演'
                if not clas_s_data['directors'] == '':
                    directors_list = clas_s_data['directors'].split(" ")
                    metadata.countries.clear()
                    for idx, dl in enumerate(directors_list):
                        metadata.directors.new().name = '{}'.format(dl)
                '演员'
                if not clas_s_data['actors'] == '':
                    actors_list = clas_s_data['actors']
                    if not len(actors_list) == 0:
                        ls = actors_list.split(',')
                        metadata.roles.clear()
                        for idx, item_list in enumerate(ls):
                            items = item_list.split('|')
                            newrole = metadata.roles.new()
                            newrole.name = '%s' % items[0]
                            Log(items)
                            if len(items) > 1:
                                isgif = items[1].split('.')
                                for i in isgif:
                                    if not i == 'gif':
                                        newrole.photo = items[1]
                '类型'
                if vid_M == 'M':
                    genre_list = clas_s_data['type']
                else:
                    genre_list = clas_s_data['type']
                    metadata.genres.clear()
                    for idx, gl in enumerate(genre_list):
                        metadata.genres.add(gl)
                '收藏集'
                if not clas_s_data['collections'] == '':
                    metadata.collections.add(clas_s_data['collections'])
                    Log(metadata.collections)
                '海报'
                if not Prefs['Poster_Cutting_Url'] == '':
                    image_url = ''
                    x = ''
                    w = ''
                    h = ''

                    if vid_M == 'M':
                        '手动搜刮海报时调用此处'
                        Log('手动搜刮海报开始写入plex库')
                        Log('开启裁切海报模式')
                        image_url = clas_s_data['imgurl']
                        x = Prefs['Poster_Cutting_X']
                        w = Prefs['Poster_Cutting_W']
                        h = Prefs['Poster_Cutting_H']

                        tmp = '%s?mode=%s&url=%s&x=%s&w=%s&h=%s' % (
                            Prefs['Poster_Cutting_Url'], vid_M, image_url,x,w,h)
                        Log(tmp)
                        poster = requests.get(tmp).content
                    if vid_M == 'A':
                        '自动搜刮海报时调用此处'
                        Log('自动搜刮海报开始写入plex库')
                        '开启裁切海报模式'
                        Log('开启裁切海报模式')
                        x = Prefs['Poster_Cutting_X']
                        w = Prefs['Poster_Cutting_W']
                        h = Prefs['Poster_Cutting_H']
                        tmp = '%s?mode=%s&url=%s&x=%s&w=%s&h=%s' % (
                            Prefs['Poster_Cutting_Url'], vid_M, clas_s_data['imgurl'][0],x,w,h)
                        Log(tmp)
                        poster = requests.get(tmp).content
                    metadata.posters[tmp] = Proxy.Media(poster)
