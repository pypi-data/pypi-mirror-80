import itertools
import typing
from urllib.parse import urlparse

from niffler.niffler import Niffler


class Erome(Niffler):
    """
    Fetch Albums from Erome. This service is out of fashion, but it's here for completeness's sake
    """

    @classmethod
    def sniff(cls, url):
        return 'erome' in urlparse(url).netloc

    def explore(self) -> typing.List[typing.Text]:
        """
        Fish images and/or video links out of Erome's album view
        """
        # Xpath is a lot easier to use than beautifulsoup when you know what you're doing.
        # It's a whole different language, which is slightly annoying,
        # But it's definitely worth learning.
        pics = self.page.html.xpath('//div[@id="album"]//img/@data-src')
        vids = self.page.html.xpath('//div[@id="album"]//video/source/@src')
        final = []
        for i in pics + vids:
            if i not in final:
                final.append(i)
        return final

