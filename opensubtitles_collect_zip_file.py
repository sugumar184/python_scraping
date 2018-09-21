# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
#import patoolib

cwd = './output/'
movie_list = []

class OpensubtitlesSpider(scrapy.Spider):
    name = 'opensubtitles_srt'
    allowed_domains = ['opensubtitles.org']
    start_urls = ['https://www.opensubtitles.org/en/search/sublanguageid-eng/movielanguage-hindi/']

    def unzip(self,file_path):
    	pass
        #patoolib.extract_archive(file_path, outdir="./zip_output")

    def parse(self, response):
        url_lists = response.xpath("//a[@class='bnone']")
        for url_list in url_lists:
            movie_name = url_list.xpath('text()').extract_first().strip()
            movie_url = url_list.xpath('@href').extract_first().strip()
            movie_url = urljoin(response.url, movie_url)
            dic = {'movie_name': movie_name, 'movie_url': movie_url}      
              ############have to change the movie_url into download url and download the file and extract
            yield scrapy.Request(movie_url, callback=self.parse_data, meta=dic)
        next_page = response.xpath("//a[@id='next']/@href").extract_first()
        if next_page is not None:
            next_page = urljoin(response.url, next_page)
            print(next_page)
            yield response.follow(next_page, callback=self.parse, headers={'Referer': 'https://www.opensubtitles.org/'})
    
    def parse_data(self, response):
        movie_name = response.meta['movie_name']
        movie_url = response.meta['movie_url']
        print('movie_name: ', movie_name)
        download_url = response.xpath(
            "//a[@class='btn btn-info downloads']/@href").extract_first().strip()
        file_formate = '.'+download_url.split('.')[-1]
        download_url = urljoin(response.url, download_url)
        file_name = cwd+movie_name+file_formate
        dic = {'movie_name': movie_name, 'movie_url': movie_url,'download_url':download_url,'file_name':file_name}
        if re.search('.rar' or '.zip', file_formate):
            yield scrapy.Request(download_url, callback=self.parse_make_req, meta=dic)
        else:    
            pass
        #yield dic
    
    def parse_make_req(self, response):
        dic_output={}
        file_name = response.meta['file_name']
        movie_name = response.meta['movie_name']
        movie_url = response.meta['movie_url']
        download_url = response.meta['download_url']
        dic_output = {'movie_name': movie_name, 'movie_url': movie_url,'download_url':download_url,'file_name':file_name}
        if not movie_name in movie_list:
            print('Downloading....: ', file_name)
            with open(file_name, "wb") as f:
                f.write(response.body)
            movie_list.append(movie_name)
            #self.unzip(file_name)
            yield dic_output
