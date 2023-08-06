import os
from functools import cached_property
from urllib.parse import urlparse

import typing

from niffler.niffler import Niffler
from niffler.gold import Media, Gold, Gallery, Page
from niffler.sites.media import MediaNiffler


class ImgurCookies(object):
    """
    Mixin for adding the NSFW cookie
    """
    cookies = (('over18', "1"),)
    # I have NO CLUE how to get this programmatically, but it seems to be
    # the anonymous client ID my desktop browser uses when I'm not logged in.
    # I seriously doubt it's at all stable. This is going to break.
    CLIENT_ID = '546c25a59c58ad7'
    headers = Gold.headers + (('Authorization', 'Client-ID {}'.format(CLIENT_ID)))


class ImgurPage(Page, ImgurCookies):
    pass


class ImgurMedia(Media, ImgurCookies):
    pass


class ImgurGallery(Gallery, ImgurCookies):
    pass


class Imgur(Niffler):
    """
    Fetch single images and albums from www.imgur.com links and i.imgur.com
    """
    page_class = ImgurPage
    media_class = ImgurMedia
    gallery_class = ImgurGallery

    def __new__(cls, url, session=None):
        # We can do a little pre-processing right off the bat and maybe save some time.
        # .gifv links are a wrapped .mp4 with a really predictable URL pattern.
        # We wont' need to explore at all in order to download them.
        if url.endswith(".gifv"):
            url = url.replace(".gifv", ".mp4")
            return MediaNiffler(url, session)
        else:
            return super(Imgur, cls).__new__(cls)

    @classmethod
    def sniff(cls, url):
        return 'imgur' in urlparse(url).netloc

    @cached_property
    def api(self):
        """
        The main gallery page, as a JSON API call

        Imgur's API has slightly different formats between a gallery and a media item, and it's hard to tell
        what we're niffling at before we fetch it.

        Try the gallery first.
        """
        post = os.path.basename(self.url)
        category = 'posts'
        url = f'https://api.imgur.com/post/v1/{category}/{post}?client_id={ImgurCookies.CLIENT_ID}&include=media'
        item = self.page_class(url, self.session)
        if not item.response.ok:
            category = 'media'
            url = f'https://api.imgur.com/post/v1/{category}/{post}?client_id={ImgurCookies.CLIENT_ID}&include=media'
            item = self.page_class(url, self.session)
        return item

    def explore(self) -> typing.List[typing.Text]:
        """
        Returns every media item in the gallery
        """
        data = self.api.response.json()
        return [m['url'] for m in data['media']]
