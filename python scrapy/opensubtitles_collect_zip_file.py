# -*- coding: utf-8 -*-
"""
use dynamic header while giving requests and check whether it is zip or rar and download it
"""
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os,io
import re,time
import zipfile
#import patoolib

cwd = './output/'
movie_list = []

class OpensubtitlesSpider(scrapy.Spider):
    name = 'opensubtitles_srt'
    allowed_domains = ['opensubtitles.org']
    start_urls = ['https://www.opensubtitles.org/en/search/sublanguageid-eng/movielanguage-hindi/']


    def parse(self, response):
        #src_id = response.url.split('-')[-1]
        #with open(src_id+'.html','wb') as f:
        #    f.write(response.body)
        #url_lists = response.xpath("//a[@class='bnone']")
        url_lists = response.xpath("//tr[contains(@class, 'expandable')]")
        for url_list in url_lists:
            movie_name = url_list.xpath(".//a[@class='bnone']/text()").extract_first().strip()
            movie_name = re.sub('\n',' ',movie_name)
            movie_url = url_list.xpath(".//a[@class='bnone']/@href").extract_first().strip()
            movie_url = urljoin(response.url, movie_url)
            movie_id = re.search('subtitles/([0-9]+)/', movie_url).group(1)
            download_url = "https://dl.opensubtitles.org/en/download/sub/"+movie_id
            imdb_url = url_list.xpath(".//a[contains(@href,'imdb')]/@href").extract_first()
            imdb_url = re.sub('/redirect/', '', imdb_url)
            dic = {'movie_name': movie_name, 'movie_url': movie_url,
                   'download_url': download_url,'imdb_url':imdb_url}
            if not movie_name in movie_list:
                movie_list.append(movie_name)
                yield dic
            #yield scrapy.Request(download_url, callback=self.parse_data, meta=dic, headers={'Referer': 'https://www.opensubtitles.org/'})
        
        next_page = response.xpath("//a[contains(text(),'>>')]/@href").extract_first()
        if next_page is not None:
            next_page = urljoin(response.url, next_page)
            #time.sleep(10)
            print('Next_page: ',next_page)
            yield response.follow(next_page, callback=self.parse,headers={'Referer': 'https://www.opensubtitles.org/'})
            
    def parse_data(self, response):
        print('entered_parse')
        dic={}
        movie_name = response.meta['movie_name']
        movie_url = response.meta['movie_url']
        download_url = response.meta['download_url']
        imdb_url = response.meta['imdb_url']
        print('movie_name: ', movie_name)
        zip_file_type = zipfile.is_zipfile(io.BytesIO(response.body))  #checking whether it is zip file or not
        cont_type = response.headers['Content-Type']                   #gives the response content type
        if zip_file_type:
            file_formate = '.zip'
        elif re.search(b'rar',cont_type):
            file_formate = '.rar'
        else:
            with open('not_zip_file.txt','a') as f:
                dic1 = {'movie_name': movie_name, 'movie_url': movie_url, 'download_url': download_url, 'file_name': file_name, 'cont_type': cont_type,'imdb_url': imdb_url}
                f.write(dic1+'\n')
            file_formate = '.txt'
        file_name = cwd+movie_name+file_formate
        dic = {'movie_name': movie_name, 'movie_url': movie_url,
               'download_url': download_url, 'file_name': file_name, 'imdb_url': imdb_url}
        if not movie_name in movie_list:
            print('Downloading....: ', file_name)
            with open(file_name, "wb") as f:
                f.write(response.body)
            movie_list.append(movie_name)
            #self.unzip(file_name)
            yield dic



############have to change the movie_url into download url and download the file and extract
#z = zipfile.is_zipfile(io.BytesIO(foo))
#r = Request('https://dl.opensubtitles.org/en/download/sub/7174228',headers={'Referer': 'https://www.opensubtitles.org/'})
