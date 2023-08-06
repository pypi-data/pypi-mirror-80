import os
import unittest

from betamax.fixtures.unittest import BetamaxTestCase
from betamax import Betamax

import niffler
from betamax_serializers.pretty_json import PrettyJSONSerializer

import niffler.gold
import niffler.sites.web

Betamax.register_serializer(PrettyJSONSerializer)


class RecordModes:
    ONCE = 'once'
    NONE = 'none'
    NEW_EPISODES = 'new_episodes'
    ALL = 'all'


CASSETTE_DIR = os.path.join(os.path.dirname(__file__), 'cassettes')
with Betamax.configure() as config:
    config.default_cassette_options['record_mode'] = RecordModes.ONCE
    config.default_cassette_options['match_requests_on'] = ['method', 'uri']
    config.default_cassette_options['serialize_with'] = 'prettyjson'
    # We're doing file comparison, so of course replay bytes exactly
    config.preserve_exact_body_bytes = True
    config.cassette_library_dir = CASSETTE_DIR


class DigTests(BetamaxTestCase):
    """
    The most fragile part of the Niffler library is the digger
    """

    @classmethod
    def setUpClass(cls) -> None:
        if not os.path.exists(CASSETTE_DIR):
            os.mkdir(CASSETTE_DIR)
        super(DigTests, cls).setUpClass()
        cls.msgs = {}

    def tearDown(self):
        self.session.close()
        super(DigTests, self).tearDown()

    def assertEqual(self, first, second, msg=None) -> None:
        msg = "\n\n" + "\n".join([
            self._testMethodName,
            f"expected = {repr(second)}"
            "----"
        ])
        super(DigTests, self).assertEqual(first, second, msg)

    def test_imgur_gallery(self):
        url = 'https://imgur.com/gallery/mA6qX6u'
        observed = niffler.dig(url, self.session)
        expected = [
            'https://i.imgur.com/QthRoLH.jpg',
            'https://i.imgur.com/BGxFNbJ.jpg',
            'https://i.imgur.com/XREpupo.jpg',
            'https://i.imgur.com/sorwBU8.jpg',
            'https://i.imgur.com/WBkd4QT.jpg',
            'https://i.imgur.com/PLmyKgg.jpg',
            'https://i.imgur.com/hsUZsWz.jpg',
            'https://i.imgur.com/1oX2CQ1.jpg',
            'https://i.imgur.com/uNjAtrg.jpg',
        ]
        self.assertEqual(expected, observed)

    def test_imgur_direct(self):
        url = 'https://i.imgur.com/pqgQrB5.jpg'
        observed = niffler.dig(url, self.session)
        expected = [url]
        self.assertEqual(expected, observed)

    def test_erome_direct(self):
        # This is a CDN link, not sure it'll be stable
        # Regardless, this won't actually hit the Erome niffler at all, I think.
        url = 'https://s2.erome.com/278/Rd6FRATd/aQMXq6O6.jpeg'
        observed = niffler.dig(url, self.session)
        expected = ['https://s2.erome.com/278/Rd6FRATd/aQMXq6O6.jpeg']
        self.assertEqual(expected, observed)

    def test_redgifs_direct(self):
        # And here's the URL of the actual content from the above two
        # note the CDN hostname. This is likely not stable.
        url = 'https://thcf6.redgifs.com/WetLegalDuiker.mp4'
        observed = niffler.dig(url, self.session)
        expected = ['https://thcf6.redgifs.com/WetLegalDuiker.mp4']
        self.assertEqual(expected, observed)

    def test_redgifs_mirrored(self):
        # Here's the same URL as the redgifs one, but note that it's mirrored on the gifdeliverynetwork.
        # GDN just embeds the RedGifs .mp4, but in a much more straightforward-to-parse way.
        url = 'https://www.gifdeliverynetwork.com/wetlegalduiker'
        observed = niffler.dig(url, self.session)
        expected = ['https://thcf6.redgifs.com/WetLegalDuiker.mp4']
        self.assertEqual(expected, observed)

    def test_imgur_gifv(self):
        url = 'https://i.imgur.com/6KYQA0W.gifv'
        observed = niffler.dig(url, self.session)
        expected = ['https://i.imgur.com/6KYQA0W.mp4']
        self.assertEqual(expected, observed)

    def test_imgur_gallery_single_item(self):
        url = 'https://imgur.com/mkBk4TI'
        observed = niffler.dig(url, self.session)
        expected = ['https://i.imgur.com/mkBk4TI.jpg']
        self.assertEqual(expected, observed)

    def test_erome_gallery(self):
        url = 'https://www.erome.com/a/pVkN0vXb'
        observed = niffler.dig(url, self.session)
        expected = ['https://s3.erome.com/278/pVkN0vXb/PQqLyfnk.png', 'https://s3.erome.com/278/pVkN0vXb/PFv3ziVh.png', 'https://s3.erome.com/278/pVkN0vXb/FLzq7GNJ.png', 'https://s3.erome.com/278/pVkN0vXb/2M5gmtoC.png', 'https://s3.erome.com/278/pVkN0vXb/0DYcK4x1.png', 'https://s3.erome.com/278/pVkN0vXb/wftbjLld.png', 'https://s3.erome.com/278/pVkN0vXb/4ORSr13J.png', 'https://s3.erome.com/278/pVkN0vXb/B9x52GZo.png', 'https://s3.erome.com/278/pVkN0vXb/md7fBPti.png', 'https://s3.erome.com/278/pVkN0vXb/prUnqP26.png', 'https://s3.erome.com/278/pVkN0vXb/O9MamLfd.png', 'https://s3.erome.com/278/pVkN0vXb/FnPTrfk2.png', 'https://s3.erome.com/278/pVkN0vXb/RGqrGZxN.png', 'https://s3.erome.com/278/pVkN0vXb/o4dyOu8s.png']
        self.assertEqual(expected, observed)

    def test_erome_gallery_single_item(self):
        url = 'https://www.erome.com/a/UAfUfHV2'
        observed = niffler.dig(url, self.session)
        expected = ['https://s2.erome.com/247/UAfUfHV2/Ml5RB7lT_480p.mp4']
        self.assertEqual(expected, observed)

    def test_redgifs(self):
        # There's a weird redirect going on with this in a browser. Make sure it resolves okay.
        url = 'https://www.redgifs.com/watch/wetlegalduiker'
        observed = niffler.dig(url, self.session)
        expected = ['https://thcf6.redgifs.com/WetLegalDuiker.mp4']
        self.assertEqual(expected, observed)

    def test_redgifs_redirect(self):
        # This is the URL that shows up in the actual browser, and might get linked to from reddit.
        # The redgifs ID is still wetlegalduiker, but there's three tags appended to it.
        url = 'https://www.redgifs.com/watch/wetlegalduiker-kitchen-nonnude-thong'
        observed = niffler.dig(url, self.session)
        expected = ['https://thcf6.redgifs.com/WetLegalDuiker.mp4']
        self.assertEqual(expected, observed)

    def test_giphycat(self):
        url = 'https://gfycat.com/finewhoppingbellsnake'
        observed = niffler.dig(url, self.session)
        expected = ['https://thcf8.redgifs.com/FineWhoppingBellsnake.mp4']
        self.assertEqual(expected, observed)

    def test_giphycat_direct(self):
        url = 'https://giant.gfycat.com/DimpledAmazingFireant.mp4'
        observed = niffler.dig(url, self.session)
        expected = ['https://giant.gfycat.com/DimpledAmazingFireant.mp4']
        self.assertEqual(expected, observed)

    def test_giphycat_mirrored(self):
        url = 'https://www.gifdeliverynetwork.com/DimpledAmazingFireant'
        observed = niffler.dig(url, self.session)
        expected = ['https://thcf2.redgifs.com/DimpledAmazingFireant.mp4']
        self.assertEqual(expected, observed)

    def test_i_reddit(self):
        url = 'https://www.reddit.com/r/funny/comments/j0w79j/the_denver_broncos_have_the_entire_town_of_south/'
        observed = niffler.dig(url, self.session)
        expected = ['https://i.redd.it/x9h34hp8iqp51.jpg']
        self.assertEqual(expected, observed)


if __name__ == '__main__':
    unittest.main()
