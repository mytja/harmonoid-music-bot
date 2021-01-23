import asyncio
import base64
import httpx
from mutagen.oggopus import OggOpus
from mutagen.flac import Picture


class Metadata(OggOpus):
    def __init__(self, trackInfo):
        self.trackInfo = trackInfo

    async def add(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, super().__init__, f"{self.trackInfo['trackId']}.ogg"
        )
        async with httpx.AsyncClient() as client:
            albumArtResponse = await client.get(self.trackInfo["albumArtHigh"])
        picture = Picture()
        picture.data = albumArtResponse.content
        """
        Initially Vorbis comments didn't contain album arts, now they can keep album arts according to FLAC's specifications, thus using Picture class from flac.
        mutagen example uses picture.type = 17 here: https://mutagen.readthedocs.io/en/latest/user/vcomment.html.
        Keeping it's value as 17 makes Android's MediaMetadataRetriever to not detect the album art.
        What on earth is "A bright coloured fish" ?
        Reference: https://xiph.org/flac/format.html#metadata_block_picture.
        """
        picture.type = 3
        picture.desc = "Cover (front)"
        picture.mime = "image/jpeg"
        picture.width = 544
        picture.height = 544
        encoded_data = base64.b64encode(picture.write())
        vcomment_value = encoded_data.decode("ascii")
        """
        Sets album art.
        """
        self["metadata_block_picture"] = [vcomment_value]
        """
        In Vorbis comments, a key e.g. "artists" can have more than one value.
        In mutagen implementation, that's why we give values in a list.
        Reference: https://gitlab.gnome.org/GNOME/rhythmbox/-/issues/16
        """
        self["title"] = [self.trackInfo["trackName"]]
        self["album"] = [self.trackInfo["albumName"]]
        """
        This is where we can simply provide simply a list of artists, as written above (for having mutiple value for the same key).     
        But, by that MediaMetadataRetriever is just shows first artist :-(. So, I'm just joining all artists with "/" separator. (Though, this is incorrect according to official reference).
        """
        self["artist"] = ["/".join(self.trackInfo["trackArtistNames"])]
        """
        No reference of this comment at http://age.hobba.nl/audio/mirroredpages/ogg-tagging.html, still using because a mutagen example uses it. Thus, unable to read.
        """
        self["albumartist"] = [self.trackInfo["albumArtistName"]]
        """
        This needs a fix. Vorbis comment keeps date instead of year & MediaMetadataRetriever is unable to read this.
        Fix if you get to know something...
        """
        self["date"] = [str(self.trackInfo["year"])]
        self["tracknumber"] = [f"{self.trackInfo['trackNumber']}/{self.trackInfo['albumLength']}"]
        """
        Again, no official reference of this one at http://age.hobba.nl/audio/mirroredpages/ogg-tagging.html. Thus, unable to read.
        """
        self["tracktotal"] = [str(self.trackInfo["albumLength"])]
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save)

        """
        Windows is unable to show Vorbis tags & album art in Windows explorer, VLC shows fine.
        """

"""
Kept old MP3 derived class.


from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TALB, TPE1, COMM, TDRC, TRCK, APIC, TPE1

class MP3(MP3):
    def __init__(self, filename, trackInfoJSON, art):
        self.filename = filename
        self.trackInfoJSON = trackInfoJSON
        self.art = art

    async def init(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, super().__init__, self.filename)

        if self.art:
            print("[metadata] Getting album art: " + self.art)
            async with httpx.AsyncClient() as client:
                response = await client.get(self.art)
            albumArtBinary = response.content
            print("[metadata] Album art retrieved.")
            self["APIC"] = APIC(
                mime="image/jpeg",
                type=3,
                desc="Cover",
                data=albumArtBinary,
            )
        else:
            print("[metadata] Album art is not found.")

        self["TIT2"] = TIT2(encoding=3, text=self.trackInfoJSON["track_name"])
        self["TALB"] = TALB(encoding=3, text=self.trackInfoJSON["album_name"])
        self["COMM"] = COMM(
            encoding=3,
            lang="eng",
            desc="https://music.youtube.com/watch?v=" + self.trackInfoJSON["track_id"],
            text="https://music.youtube.com/watch?v=" + self.trackInfoJSON["track_id"],
        )
        self["TPE1"] = TPE1(
            encoding=3, text="/".join(self.trackInfoJSON["track_artists"])
        )
        if len(self.trackInfoJSON["album_artists"]) != 0:
            self["TPE2"] = TPE2(encoding=3, text=self.trackInfoJSON["album_artists"][0])
        self["TDRC"] = TDRC(encoding=3, text=self.trackInfoJSON["year"])
        self["TRCK"] = TRCK(encoding=3, text=str(self.trackInfoJSON["track_number"]))

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save)
"""
