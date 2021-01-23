from .browsing import BrowsingHandler
from .downloading import DownloadHandler
from .async_pytube_ytmusicapi import YTMusic



class HarmonoidService(BrowsingHandler, DownloadHandler):
    ytMusic = YTMusic()
