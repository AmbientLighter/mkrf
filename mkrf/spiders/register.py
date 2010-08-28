#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from mkrf.items import *

def trim(s):
    if not isinstance(s, basestring):
        return s
    return re.sub("\s+", " ", s)

from scrapy.contrib.loader.processor import TakeFirst
class RegisterLoader(XPathItemLoader):
    default_input_processor = MapCompose(trim)
    default_output_processor = TakeFirst()
    
class RegisterSpider(BaseSpider):
    domain_name = 'mkrf.ru'
    start_urls = ['http://mkrf.ru/activity/register/search/']
    item_links = SgmlLinkExtractor(allow='detail.php')
    pages = SgmlLinkExtractor(restrict_xpaths="//a[contains(., 'След')]")

    def parse(self, response):
        return FormRequest.from_response(response, formnumber=1, callback=self.parse_index)
        
    def parse_index(self, response):
        for link in self.item_links.extract_links(response):
            yield Request(link.url, self.parse_item)
            
        for link in self.pages.extract_links(response):
            yield Request(link.url, self.parse_index)
            
    def parse_item(self, response, blocked=False):
        def td(s):
            return './/td[contains(b,"%s")]/following-sibling::td/text()' % s
        def extract_id():
            id = re.search("ID=(\d{6,})", response.url).group(1)
            return id
        xs = HtmlXPathSelector(response)
        try:
            table = xs.select('//div[@class="inner_left"]/table[1]')[0]
            
            l = RegisterLoader(FilmItem(), table)
            for key, field in FilmItem.fields.items():
                txt = field.get('txt')
                if not txt:
                    continue
                l.add_xpath(key, td(txt))
            l.add_value('id', extract_id())
            l.add_value('blocked', int(blocked))
            yield l.load_item()
            
            for table in xs.select('//table')[2:]:
                l = RegisterLoader(LicenseItem(), table)
                for key, field in LicenseItem.fields.items():
                    txt = field.get('txt')
                    if not txt:
                        continue
                    l.add_xpath(key, td(txt))
                l.add_value('id', extract_id())
                yield l.load_item()
                
        except IndexError:
            yield FormRequest.from_response(response, formnumber=1, 
                clickdata={'name':'YES'}, callback=lambda r: self.parse_item(r, True))
        
SPIDER = RegisterSpider()
