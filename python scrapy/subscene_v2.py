# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
import io
import zipfile

output_dir = './output/'
class SubsceneSpider(scrapy.Spider):
    name = 'subscene1'
    allowed_domains = ['sub.tikfilm.org']
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY' : 2,
        'CONCURRENT_REQUESTS':1,
        'AUTOTHROTTLE_ENABLED':True
    }
    def start_requests(self):
        with open('input.txt', 'r') as f:
            list_url = f.readlines()
            #list_url = [line.rstrip() for line in f]
        for i in list_url:
            movie_name,url = i.split('\t')
            url = url.strip()
            page_src = self.check_url(url)
            if page_src == 'list_page':
                url = url+'/english'
            url = re.sub('https://subscene.com','http://sub.tikfilm.org',url)
            yield scrapy.Request(url, meta={'movie_name': movie_name,'page_src':page_src}, callback=self.parse,errback=self.errback_httpbin,dont_filter=True)
    def check_url(self,url):
        a = re.search(r'/english/\d+$', url)        #tell the url is direct page
        b = re.search('/english',url)       #tell the url is list_page
        if a is not None:
            return 'direct'
        elif b is  None:
            return 'list_page'
    def errback_httpbin(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            url = response.url
            meta = response.request.meta
        yield scrapy.Request(url, meta=meta, callback=self.parse,errback=self.errback_httpbin,dont_filter=True)
    def parse(self, response):
        movie_name = response.meta['movie_name']
        page_src = response.meta['page_src']
        movie_url = response.url
        if page_src == 'direct':
            header_tag = response.xpath("//div[@class='header']/*[self::h1 or self::h2]")
            output_movie_name = header_tag.xpath("./span[@itemprop='name']/text()").extract_first().strip()     ### h1 tag
            if output_movie_name is None:
                output_movie_name = header_tag.xpath("./text()").extract_first().strip()
            imdb_url = header_tag.xpath("./a[@class='imdb']/@href").extract_first(default='not-found').strip()
            download_url = response.xpath("//a[@id='downloadButton']/@href").extract_first().strip()
            if download_url is not None:
                download_url = urljoin(response.url, download_url)
                dic = {'movie_name': movie_name, 'output_movie_name': output_movie_name,
                       'download_url': download_url, 'imdb_url': imdb_url,'movie_url': movie_url}
                yield scrapy.Request(download_url, callback=self.download, meta=dic, headers={'Referer': 'http://sub.tikfilm.org'})
        elif page_src == 'list_page':
            empty = response.xpath("//td[@class='empty']")
            output_movie_name = response.xpath("//div[@class='header']/*[self::h1 or self::h2]/text()").extract_first().strip()
            if len(empty) ==0:
                sub_url = response.xpath("//td[@class='a1']/a/@href").extract_first()
                sub_url = urljoin(response.url, sub_url)
                yield scrapy.Request(sub_url, callback=self.parse, meta={'movie_name': movie_name, 'page_src': 'direct'}, headers={'Referer': 'http://sub.tikfilm.org'})
            else:
                yield {'movie_name': movie_name, 'output_movie_name': output_movie_name, 'download_url': '', 'imdb_url': '', 'movie_url': movie_url}
    def download(self,response):
        movie_name = response.meta['movie_name']
        output_movie_name = response.meta['output_movie_name']
        download_url = response.meta['download_url']
        imdb_url = response.meta['imdb_url']
        movie_url = response.meta['movie_url']
        print('Movie_name:', movie_name)
        dic = {'movie_name': movie_name, 'output_movie_name': output_movie_name,
               'download_url': download_url, 'imdb_url': imdb_url, 'movie_url': movie_url}
        # checking whether it is zip file or not
        zip_file_type = zipfile.is_zipfile(io.BytesIO(response.body))
        # gives the response content type
        cont_type = response.headers['Content-Type']
        if zip_file_type:
            file_formate = '.zip'
        elif re.search(b'rar', cont_type):
            file_formate = '.rar'
        else:
            with open('not_zip_file.txt', 'a') as f:
                f.write(dic+'\n')
            file_formate = '.txt'
        filename = output_dir+movie_name+file_formate
        with open(filename, 'wb') as f:       
            f.write(response.body)
        
        yield dic
