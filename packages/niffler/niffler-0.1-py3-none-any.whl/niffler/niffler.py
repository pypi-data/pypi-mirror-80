from functools import cached_property
from pathlib import Path

import typing

import requests

from niffler.gold import Media, Gold, Gallery, Page, FoolsGold


class Niffler(object):
    """
    Parse a page, and extract its content.

    Maybe try a bunch of mirrors.
    """
    page_class = Page
    media_class = Media
    gallery_class = Gallery

    def __init__(self, url, session=None):
        self.url = url
        self.session = session or requests.Session()

    @classmethod
    def sniff(cls, url):
        """
        Returns False when this Niffler type isn't even worth trying on this URL.
        """
        # This core Niffler class won't save anything, since it does... nothing.
        # It will still work fine if invoked directly, but it won't be dispatched.
        return False

    @cached_property
    def page(self) -> 'Page':
        """
        The page a niffler is going to dig around on.
        """
        return self.page_class(self.url, self.session)

    def explore(self) -> typing.List[typing.Text]:
        """
        Returns where we might find the good stuff on the page.

        Will (probably) do at least one network request to pull down the .page content; maybe several if it needs to
        follow any intermediate links all the way down.
        """
        raise NotImplementedError("Nifflers do nothing until you've trained them")

    def dig_up(self) -> Gold:
        """
        Returns a promise-style wrapper object for the "good stuff" off the page.

        Unless we're already targeting a direct media URL, this will probably do a network request to scrape a page, but
        it probably *won't* have done the network request(s)to actually pull down the item content. We've saved as much
        bandwidth as we could.
        """
        if self.media_class.is_media(self.url):
            # No digging required! We were handed gold already.
            return self.media_class(self.url, self.session)

        # Not directly media. Some digging required
        urls = self.explore()
        if not urls:
            # Found nothing :(
            return FoolsGold(self.url, self.session)

        if len(urls) == 1:
            # One thing: return just that thing
            return self.media_class(urls[0], self.session)

        else:
            # Lots of things: Return a Gallery of everything we found
            media = [self.media_class(u) for u in urls]
            return self.gallery_class(url=self.url, session=self.session, more=media)

    @cached_property
    def gold(self) -> Gold:
        return self.dig_up()

    # Proxy save method to the item we .dig() up
    def save_in(self, folder: Path, overwrite=False):
        return self.gold.save_in(folder, overwrite=overwrite)
