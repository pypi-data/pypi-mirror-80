import typing
from urllib.parse import urlparse
from functools import cached_property

from niffler.niffler import Niffler
from niffler.gold import Page, Gold


class SelfPost(Page):

    @cached_property
    def text(self) -> typing.Text:
        """
        The text of a self-post
        """
        data = self.response.json()
        post = data[0]['data']['children'][0]['data']
        sections = [post['title'], post['author'], post['selftext']]
        return "\n\n".join(sections)

    @cached_property
    def bytes(self) -> bytes:
        return self.text.encode('UTF-8')

    def json(self):
        return self.response.json()


class Reddit(Niffler):
    """
    Figure out what content we want to save from a reddit post.

    Maybe a self post? Or (more likely) the linked content.
    """

    @classmethod
    def sniff(cls, url):
        url = urlparse(url)
        return bool("reddit.com" in url.netloc)

    def api_url(self) -> typing.Text:
        """
        Each old.reddit.com or www.reddit.com page has a corresponding public read-only api.reddit.com page
        """
        url = urlparse(self.url)
        url = url._replace(scheme="https", netloc='api.reddit.com').geturl()
        return url

    @cached_property
    def page(self) -> SelfPost:
        """
        JSON is way easier to deal with than anything scraping-related; the SelfPost class supplies that as long
        as we hit the reddit API url instead of whatever we were originally fed.
        """
        api_url = self.api_url()
        return SelfPost(api_url, session=self.session)

    def post_info(self):
        """
        The actually interesting part of the reddit post (not the comments)
        """
        post = self.page.json()[0]['data']['children'][0]['data']
        return post

    def explore(self) -> typing.List[typing.Text]:
        post = self.post_info()
        if post['selftext']:
            # We're already here. Don't recurse further.
            return [self.api_url()]
        else:
            # Recurse into another Niffler. We don't know what lies ahead.
            # Circular import alert :(
            from niffler.sites.web import WebNiffler
            return WebNiffler(post['url']).explore()

    def dig_up(self) -> Gold:
        """
        Self posts are handled directly. All others are delegated
        """
        post = self.post_info()
        if post['selftext']:
            # The API call page we've been looking at can render the .bytes of a self post
            # The .response is already pre-fetched and stuff too!
            return self.page
        else:
            from niffler.sites.web import WebNiffler
            return WebNiffler(post['url']).dig_up()
