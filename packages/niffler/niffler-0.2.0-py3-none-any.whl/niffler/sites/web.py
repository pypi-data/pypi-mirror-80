import typing

from niffler.niffler import Niffler
from niffler.sites.erome import Erome
from niffler.sites.giphdeliverynetwork import GifDeliveryNetwork
from niffler.sites.giphycat import Giphycat
from niffler.sites.imgur import Imgur
from niffler.sites.media import MediaNiffler
from niffler.sites.reddit import Reddit
from niffler.sites.redgifs import Redgifs

__all__ = ['WebNiffler']


class WebNiffler(Niffler):
    """
    Grab the good stuff off the page, no matter what kind of page it is.
    """
    classes = (
        # This niffler handles all direct links! First thing to try always.
        MediaNiffler,
        # These handle indirect links (media on a splash-page)
        Imgur,
        Erome,
        Giphycat,
        Redgifs,
        GifDeliveryNetwork,
        # This handles self-posts directly, and follows other URLs it sees.
        # It re-delegates back here for non-self-posts.
        Reddit,
    )

    def explore(self) -> typing.List[typing.Text]:
        """
        Try several nifflers, one after the other.

        Exactly one Niffler should, eventually, work.
        """
        for c in self.classes:
            if c.sniff(self.url):
                hunter = c(self.url, self.session)
                found = hunter.explore()
                if found:
                    return found

        return []
