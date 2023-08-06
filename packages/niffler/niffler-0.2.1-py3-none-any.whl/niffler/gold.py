import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from lxml import etree
from functools import cached_property


class Gold(object):
    """
    An item we want to download, and maybe save. It contains:

        - url - what a human would load in a web browser address bar to get the item
        - response - the network response for the one nugget of goodness we actually wanted to fetch
        - content - bytes of a file we'll write to disk based on that network response
    """
    # Class variables sent with every flavor of request
    # Impersonate a browser.
    headers = (
        (
            "User-Agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 "
            "Safari/537.36 OPR/54.0.2952.64",
        ),
        (
            "Accept",
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/webp,image/apng,*/*;q=0.8",
        ),
        ("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.3"),
        ("Accept-Encoding", "none"),
        ("Accept-Language", "en-US,en;q=0.8"),
        ("Connection", "keep-alive"),
    )
    cookies = tuple()

    def __init__(self, url, session=None, more=None):
        self.url = url
        self.session = session or requests.Session()
        self.more = more or []


    # Immutable calculated attributes based on the URL.
    @cached_property
    def response(self) -> requests.Response:
        """
        The response to a .get() request at the wrapped URL.
        """
        # If you need to do want to do URL mangling, page parsing, redirect following, etc.
        # do it here.
        r = self.session.get(
            self.url, headers=dict(self.headers), cookies=dict(self.cookies)
        )
        return r

    @cached_property
    def bytes(self) -> bytes:
        """
        Returns the bytes we'd save to disk if we chose to
        """
        # If you need to do any post-response content mangling, do it here.
        return self.response.content or b''

    @cached_property
    def basename(self):
        """
        Return exactly where we'd save this item if we chose to.

        This will probably hit the network and crawl. A Niffler doesn't initially know what it's going to find, only
        where to start looking. A-priori, we can't determine final Media file name unless our target URL is obviously
        pointing directly a piece of media.
        """
        return os.path.basename(self.url)

    @cached_property
    def media_urls(self):
        return [self.url]

    def save_in(self, folder: Path, overwrite=False):
        """
        Save this item *in* the target folder, not *as* the target file.
        """
        file = folder.joinpath(self.basename)
        if file.exists() and not overwrite:
            return

        if not self.bytes:
            return

        with file.open('wb') as fh:
            fh.write(self.bytes)


class Page(Gold):
    """
    An HTML page we might want to save
    """

    @cached_property
    def html(self):
        """
        The bytes of the page represented as an HTML-based lxml.ElementTree

        This will for sure blow up if we're not wrapping an HTML page.

        Super useful for scraping the wrapped page to return something more interesting at .media
        """
        return etree.HTML(self.response.content)

    @cached_property
    def soup(self):
        """
        A BeautifulSoup object we can use for parsing, if we want to.
        """
        return BeautifulSoup(self.response.text, features="html.parser")


class FoolsGold(Gold):
    """
    Looks like gold to a niffler (and automatic processing utilities), but is actually garbage.

    Sometimes we know early on in the search process we can't continue, but we want to defer raising an exception until
    we've done more (probably parallel) processing. a fake bad response. Usually when a preliminary request successfully got some
    human-readable landing page, but there is nothing worth downloading on it.

    So instead of returning the successful landing page response with nothing useful, we return this error.

    This item will always appear like we've made a network request and failed, but actually will never hit the network.
    """

    # Not cached properties, since Bad() is a singleton. We'll return a different Response() object every time
    # from each place it's called.
    @property
    def bytes(self) -> bytes:
        return b''

    @property
    def response(self) -> requests.Response:
        """
        Make a response that looks like an HTTP request returned an error.

        We use the "418" status code, because making any further network requests would be about as useful as asking a
        teapot to make coffee. So we pretend that's what happened.
        """
        r = requests.Response()
        r.status_code = 418
        r.reason = "I'm a teapot (RFC 2324)"
        return r

    def save_in(self, folder: Path, overwrite=False):
        """
        Don't ever save a bad request. But don't die either.
        """
        return


class Gallery(Gold):
    """
    Some pages can have a bunch of items on them. We'll save them all. We use nested Items to do that

    The top-level item is a "cover page". It has the response of the main gallery page, but the .bytes of the
    first object in the gallery.

    The top-level item has a `.more` attribute with all the media.
    """

    @classmethod
    def maybe(cls, page_url, more, session=None):
        # Don't always construct a Gallery object if it won't make any sense. Swap it out instead.
        if len(more) == 0:
            return FoolsGold(page_url, session)

        if len(more) == 1:
            return more[0]

        else:
            return cls(page_url, session, more)

    @cached_property
    def media_urls(self):
        return [g.url for g in self.more]

    def save_in(self, folder: Path, overwrite=False, merge=True):
        """
        Save the gallery as a nested folder *in* the target folder. Don't just plop items down.
        """
        # Shouldn't be a single file's extension.
        if not self.more:
            return

        # If this is really a gallery, basename will probably be 'abcd1234 from a url like .../album/abcd1234/
        gallery = folder.joinpath(self.basename)
        gallery.mkdir(exist_ok=merge)
        for item in self.more:
            item.save_in(gallery, overwrite)


class Media(Gold):
    """
    Basic downloader class for a single image or video. Saves exactly what we find at URL as an Item.

    Won't try downloading anything if the URL doesn't appear to point at an image or video.
    """

    @classmethod
    def maybe(cls, url, session):
        # Don't bother constructing an Item for something we wont' be able to download.
        if cls.is_media(url):
            return cls(url, session)

        else:
            return FoolsGold(url, session)

    media_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".jpe",
        ".jfif",
        ".jfi",
        ".bmp",
        ".gif",
        ".gfy",
        ".webm",
        ".webp",
        ".tif",
        ".tiff",
        ".bmp",
        ".dib",
        ".mp4",
    )

    @classmethod
    def is_media(cls, url):
        """
        Returns True if the URL appears to be a direct link to some kind of interesting file we definitely want
        """
        return bool(Path(url).suffix in cls.media_extensions)

    @cached_property
    def response(self) -> requests.Response:
        """
        Refuse to even send a network request if it doesn't look like a media item.

        __new__ should have caught this... but maybe not?
        """
        if self.is_media(self.url):
            return super(Media, self).response

        else:
            return FoolsGold(self.url, self.session).response
