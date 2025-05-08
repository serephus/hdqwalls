# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.http import TextResponse

from ..items import HdqwallsItem


class Hdqwalls(scrapy.Spider):
    name = "hdqwalls"
    allowed_domains = ['hdqwalls.com']
    start_urls = ['https://hdqwalls.com/latest-wallpapers/page/1']

    def parse(self, response: TextResponse):
        # let scrapy deduplicate urls for us
        for next in response.css('ul.pagination li a::attr(href)'):
            yield response.follow(next, callback=self.parse)

        image_urls = [
            # the origin url is just thumb url without the thumb part
            wallpaper.css('img::attr(src)').get().replace("thumb/", "")
            for wallpaper in response.css('div.wallpapers_container div.wall-resp')
        ]
        yield HdqwallsItem(image_urls=image_urls)
