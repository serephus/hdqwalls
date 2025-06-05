# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from typing import Generator, Optional

from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.spiders import Spider

from ..items import HdqwallsItem


class Hdqwalls(Spider):
    name = "hdqwalls"
    allowed_domains = ["hdqwalls.com"]
    start_urls = ["https://hdqwalls.com/latest-wallpapers/page/1"]

    def parse(self, response: Response) -> Generator[Request | HdqwallsItem]:
        # let scrapy deduplicate page urls for us
        # pages: Iterable[str] = response.css("ul.pagination li a::attr(href)")
        for page in response.css("ul.pagination li a::attr(href)"):
            url: Optional[str] = page.get()
            if url is None:
                continue
            yield response.follow(url, callback=self.parse)

        image_urls = [
            # the origin url is just thumb url without the thumb part
            url.replace("thumb/", "")
            for wallpaper in response.css(
                "div.wallpapers_container div.wall-resp"
            )
            if (url := wallpaper.css("img::attr(src)").get()) is not None
        ]
        yield HdqwallsItem(image_urls=image_urls)
