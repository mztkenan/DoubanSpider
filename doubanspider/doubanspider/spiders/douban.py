# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from ..items import DoubanspiderItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    #start_urls = ['https://movie.douban.com/subject/26861685/comments?status=P']
    bash_url='https://movie.douban.com/subject/'#33位
    end_url='/comments'#9位

    def start_requests(self):
        # for i in  range(3445906,3445907):
        for i in  range(1301066, 27000000):
            url=self.bash_url+str(i)+self.end_url
            yield Request(url, self.parse)

    def parse(self, response):
        film_name=str(response.xpath('//*[@id="content"]/h1/text()').extract()[0])[:-3]
        item=DoubanspiderItem()
        comments=response.xpath('//div[@class="mod-bd"]/div[@class="comment-item"]')
        for content in comments:
            result=content.xpath('.//span[contains(@class,"allstar")]/@title').extract() #容错，评分有可能没有，没有的不做记录
            if result:
                score=str(result[0])
                if score=='力荐':
                    item['score'] = '5'
                elif score=='推荐':
                    item['score'] = '4'
                elif score=='还行':
                    item['score'] = '3'
                elif score=='较差':
                    item['score'] = '2'
                elif score=='很差':
                    item['score'] = '1'
                item['username'] = content.xpath('.//span[@class="comment-info"]/a/text()').extract()
                item['name']=film_name
                yield item
        next_url = response.xpath('//a[@class="next"]/@href').extract()
        if next_url:
            next_url = str(response.url)[:49]+next_url[0]  #拼接前面的字符串，切片不包含51
            yield Request(next_url)
