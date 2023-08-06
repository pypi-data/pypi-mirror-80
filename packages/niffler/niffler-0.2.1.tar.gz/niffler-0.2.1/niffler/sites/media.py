import typing

from niffler.gold import Media, Gold
from niffler.niffler import Niffler

__all__ = ['MediaNiffler']


class MediaNiffler(Niffler):
    """
    Directly downloads the media you point at it.

    ... or tries to, anyway.
    """

    @classmethod
    def sniff(cls, url):
        return Media.is_media(url)

    def explore(self) -> typing.List[typing.Text]:
        """
        Looks at the URL directly to decide if it's already media we can download
        """
        if Media.is_media(self.url):
            return [self.url]

        else:
            return []
