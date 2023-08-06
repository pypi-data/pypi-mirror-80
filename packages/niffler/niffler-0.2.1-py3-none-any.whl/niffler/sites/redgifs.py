import json
import re
from urllib.parse import urlparse

import typing
from bs4 import BeautifulSoup

from niffler.niffler import Niffler
from niffler.sites.giphdeliverynetwork import GifDeliveryNetwork
from niffler.gold import Gold


class Redgifs(Niffler):
    """
    Fetch single images from redgifs
    """

    @classmethod
    def sniff(cls, url):
        return 'redgifs' in urlparse(url).netloc

    def __init__(self, *args, **kwargs):
        super(Redgifs, self).__init__(*args, **kwargs)

    def explore(self) -> typing.List[typing.Text]:
        return self.from_mirror()

    def from_page(self) -> typing.List[typing.Text]:
        """
        Very commonly, we'll have to parse a landing page to get the video
        """
        # This does not appear to work right now
        page = Gold(self.url, self.session)
        soup = BeautifulSoup(page.response.text, "html.parser")
        attributes = {"data-react-helmet": "true", "type": "application/ld+json"}
        script = soup.find("script", attrs=attributes)
        if script:
            video_url = json.loads(script)["video"]["contentUrl"]
            return [video_url]

        return []

    def from_mirror(self) -> typing.List[typing.Text]:
        """
        GDN mirrors redgifs stuff too, you just have to fish the ID out of the redgifs URL
        """
        match = re.search("/watch/(\w+)/?", self.url)
        if match:
            id = match.group(1)
            backup_path = "https://www.gifdeliverynetwork.com/" + id
            return GifDeliveryNetwork(backup_path, self.session).explore()

        return []
