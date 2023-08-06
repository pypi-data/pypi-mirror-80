from urllib.parse import urlparse

import typing
from bs4 import BeautifulSoup

from niffler.niffler import Niffler


class GifDeliveryNetwork(Niffler):
    """
    The Gif Delivery Network is a fallback system we can use in a lot of cases where stuff is gone from the primary
    source. They mirror old stuff from Giphy and Redgifs
    """

    @classmethod
    def sniff(cls, url):
        return 'gifdeliverynetwork.com' in urlparse(url).netloc

    def explore(self) -> typing.List[typing.Text]:
        """
        Extract the video content from the page's source and return it
        """
        attributes = {"id": "mp4Source", "type": "video/mp4"}
        content = self.page.soup.find("source", attrs=attributes)
        return [content['src']]
