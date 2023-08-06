import json
from urllib.parse import urlparse

import typing

from niffler.niffler import Niffler
from niffler.sites.giphdeliverynetwork import GifDeliveryNetwork


class Giphycat(Niffler):
    """
    Fetch videos from giphycat
    """

    @classmethod
    def sniff(cls, url):
        return 'gfy' in urlparse(url).netloc

    def from_page(self) -> typing.List[typing.Text]:
        """
        Maybe there's a video content URL on a this browsable Giphycat page?
        """
        # This is just like... not working right now
        soup = self.page.soup
        attributes = {"data-react-helmet": "true", "type": "application/ld+json"}
        script = soup.find("script", attrs=attributes)
        if script:
            content_url = json.loads(script.contents[0])["video"]["contentUrl"]
            return [content_url]

        return []

    def from_mirror(self) -> typing.List[typing.Text]:
        """
        Maybe it's on Gif Delivery Network, a mirror for Giphycat?
        """
        # If our primary source fails, we can sometimes find old gifs on GDN
        giphycat = urlparse(self.url)
        backup_path = "https://www.gifdeliverynetwork.com" + giphycat.path
        return GifDeliveryNetwork(backup_path, self.session).explore()

    def explore(self):
        """
        There are two possible ways to get a Giphycat video
        """
        return self.from_mirror()
