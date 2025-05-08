# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
from typing import Optional

# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.media import MediaPipeline
from scrapy.http import Request, Response

from .items import HdqwallsItem


class HdqwallsPipeline(ImagesPipeline):
    def file_path(
        self,
        request: Request,
        response: Optional[Response] = None,
        info: Optional[MediaPipeline.SpiderInfo] = None,
        *,
        item: Optional[HdqwallsItem] = None
    ) -> str:
        hash = hashlib.sha1(request.url.encode()).hexdigest()
        name = ".".join(request.url.split("/")[-1].split(".")[:-1])
        return f"full/{hash}-{name}.jpg"
