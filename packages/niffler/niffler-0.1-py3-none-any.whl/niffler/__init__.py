import argparse
import os
import sys
import typing

from pathlib import Path

import requests

from niffler.gold import Gold
from niffler.sites.web import WebNiffler
from niffler.niffler import Niffler


def dig(url, session=None) -> typing.List[typing.Text]:
    """
    Use a WebNiffler (which should be able to find anything) to dig for the content implied by URL.
    """
    niff = WebNiffler(url, session=session)
    urls = niff.explore()
    return urls


def save_in(url, to_folder: str, session=None) -> None:
    """
    Use a WebNiffler to save the media found in URL to the folder indicated.
    """
    niff = WebNiffler(url, session=session)
    niff.gold.response.raise_for_status()
    to_folder = Path(to_folder)
    niff.gold.save_in(to_folder)


def cli():
    argv = sys.argv[1:]
    """Command-line interface for the niffler"""
    parser = argparse.ArgumentParser(
        description="Find and download media from a specific URL"
    )
    parser.add_argument('urls', nargs='+', help="The URLs to search for content")
    # When "-s" with no arg is passed, save in the current working directory.
    # When "-s" with one arg is passed, save there
    parser.add_argument(
        '-s',
        '--save_in',
        metavar="F",
        nargs='?',
        default=None,
        const=os.getcwd(),
        help="Save media you find in this folder",
    )
    parser.add_argument(
        '-v', '--verbose', action='count', default=0, help="Display logs to STDERR"
    )
    namespace = parser.parse_args(argv)
    with requests.Session() as session:
        for u in namespace.urls:
            if namespace.save_in:
                save_in(u, to_folder=namespace.save_in, session=session)
            else:
                urls = dig(u, session=session)
                for u in urls:
                    print(u)
                if not urls:
                    sys.stderr.write('Nothing found\n')


__all__ = ['Niffler', 'WebNiffler', 'dig', 'save_in']
