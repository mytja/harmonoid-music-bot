from .browsing import BrowsingHandler
from .downloading import DownloadHandler
from .async_pytube_ytmusicapi import YTMusic, YouTube



class HarmonoidService(BrowsingHandler, DownloadHandler):
    ytMusic = YTMusic()
    youtube = YouTube()
    browsingHandler = BrowsingHandler()
