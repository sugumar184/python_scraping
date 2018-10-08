# -*- coding: utf-8 -*-
'''
get url and movie name  from the  input.txt file and loop through the input.txt and use start_requests function 
download the zip file
'''
import scrapy
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re

output_dir = './output/'
class SubsceneSpider(scrapy.Spider):
    name = 'subscene1'
    allowed_domains = ['subscene.com/']
    def start_requests(self):
        with open('input.txt', 'r') as f:
            list_url = f.readlines()
            #list_url = [line.rstrip() for line in f]
        for i in list_url:
            movie_name,url = i.split('\t')
            url = url.strip()
            yield scrapy.Request(url, meta={'movie_name': movie_name})

    def parse(self, response):
        movie_name = response.meta['movie_name']
        header_tag = response.xpath("//div[@class='header']/*[self::h1 or self::h2]")
        output_movie_name = header_tag.xpath("./span[@itemprop='name']/text()").extract_first().strip()     ### h1 tag
        if output_movie_name is None:
            output_movie_name = header_tag.xpath("./text()").extract_first().strip()
        imdb_url = header_tag.xpath("./a[@class='imdb']/@href").extract_first().strip()
        download_url = response.xpath("//a[@id='downloadButton']/@href").extract_first().strip()
        if download_url is not None:
            download_url = urljoin(response.url, download_url)
            dic = {'movie_name': movie_name, 'output_movie_name': output_movie_name,
                   'download_url': download_url, 'imdb_url': imdb_url}
            yield scrapy.Request(download_url, callback=self.download, meta=dic)

    def download(self,response):
        movie_name = response.meta['movie_name']
        output_movie_name = response.meta['output_movie_name']
        download_url = response.meta['download_url']
        imdb_url = response.meta['imdb_url']
        filename = output_dir+movie_name+'.zip'
        print('file_name :',filename)
        with open(filename, 'wb') as f:       
            f.write(response.body)
        dic = {'movie_name': movie_name, 'output_movie_name': output_movie_name,
               'download_url': download_url, 'imdb_url': imdb_url}
        yield dic
