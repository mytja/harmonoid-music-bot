import httpx
import subprocess
import aiofiles
import aiofiles.os
import os
import sys
import asyncio
import ytmusicapi
from pytube import YouTube
from .async_mutagen import Metadata

MUSICAPI_VERSION = ytmusicapi.__version__
FFMPEG_COMMAND = 'ffmpeg -i {trackId}.webm -vn -c:a copy {trackId}.ogg'


class DownloadHandler:
    async def trackDownload(self, trackId, albumId, trackName):
        if trackId:
            print(f"[server] Download request in ID format.")
        if trackName:
            print(f"[server] Download request in name format.")
            trackId = await self.ytMusic.searchYoutube(trackName, "songs")
            trackId = trackId[0]["videoId"]
        if os.path.isfile(f"{trackId}.ogg"):
            print(
                f"[pytube] Track already downloaded for track ID: {trackId}.\n[server] Sending audio binary for track ID: {trackId}."
            )
            return trackId+".ogg"

        trackInfo = await self.trackInfo(trackId, albumId)
        if type(trackInfo) is dict:
            print(
                f"[ytmusicapi] Successfully retrieved metadata of track ID: {trackId}."
            )
            await self.saveAudio(trackInfo, metadataAdd=True)
            print(f"[server] Sending audio binary for track ID: {trackId}")
            return trackId+".ogg"
        else:
            print(f"[ytmusicapi] Could not retrieve metadata of track ID: {trackId}.")
            print(f"[server] Sending status code 500 for track ID: {trackId}.")
            return 500

    async def YTdownload(self, trackName, author):
        if trackName:
            print(f"[server] Download request in name format.")
            try:
                result = self.browsingHandler.searchYT(trackName)
                result = result["result"][0]
            except Exception as e:
                print(f"[track-search] {e}")
                return
        
        url = "https://youtube.com/watch?v="+result["id"]
        print("[url] "+url)
        
        trackId = result["id"]
        
        trackInfo = {
            "trackId": trackId,
            "url": url,
            "filename": trackId+".ogg",
            "thumbnail": result["thumbnails"][0]["url"],
            "duration": result["duration"],
            "opusTrackName": trackId+".webm",
            "title": result["title"],
            "author": author
        }
        print(trackInfo)
        
        
        if os.path.isfile(f"{trackId}.ogg"):
            print(
                f"[pytube] Track already downloaded for track ID: {trackId}.\n[server] Sending audio binary for track ID: {trackId}."
            )
            return trackId+".ogg"
            
        
        filename = trackId
        
        YouTube(url).streams.get_by_itag(251).download(filename = trackInfo["trackId"])
        
        try:
            await self.ffmpeg_conv(trackInfo)
        except Exception as e:
            print(f"[ffmpeg-conv] {e}")

        print(f"[server] Sending audio binary for track ID: {trackId}")
        return trackInfo

    async def ffmpeg_conv(self, trackInfo):
        process = subprocess.Popen(
            FFMPEG_COMMAND.format(trackId=trackInfo["trackId"]),
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        while process.poll() is None:
            await asyncio.sleep(0.1)
        _, stderr = process.communicate()
        stderr = stderr.decode()

        if process.poll() != 0:
            print("[stderr]", stderr)

        asyncio.ensure_future(aiofiles.os.remove(f"{trackInfo['trackId']}.webm"))

    async def saveAudio(self, trackInfo, metadataAdd):
        filename = f"{trackInfo['trackId']}.webm"
        print(f"[httpx] Downloading track ID: {trackInfo['trackId']}.")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                trackInfo["url"], timeout=None, headers={"Range": "bytes=0-"}
            )
        if response.status_code in [200, 206]:
            async with aiofiles.open(filename, "wb") as file:
                await file.write(response.content)
            """
            WEBM container preferred for video files, but who thought YouTube would store only audio in it. (Similar case is with the 140 stream).
            So, we have no choice but to use another container for OPUS which supports adding audio tags.
            Changing WEBM Matroska container to OGG without re-encoding (to add vorbis comments on OGG container).
            """
            process = subprocess.Popen(
                FFMPEG_COMMAND.format(trackId=trackInfo["trackId"]),
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )
            while process.poll() is None:
                await asyncio.sleep(0.1)
            _, stderr = process.communicate()
            stderr = stderr.decode()

            if process.poll() != 0:
                print("[stderr]", stderr)

            """
            It's not important, so we can do it in background.
            """
            asyncio.ensure_future(aiofiles.os.remove(f"{trackInfo['trackId']}.webm"))
            """
            Adding metadata.
            """
            if metadataAdd == True:
                await Metadata(trackInfo).add()
            else:
                print("Skipping metadata adding!")
            print(
                f"[pytube] Track download successful for track ID: {trackInfo['trackId']}."
            )
        else:
            print(f"[pytube] Could not download track ID: {trackInfo['trackId']}.")
            print(
                f"[server] Sending status code 500 for track ID: {trackInfo['trackId']}."
            )
            return 500

    """
    Yet to implement...
    """
    async def updateYTMusicAPI(self):
        async with httpx.AsyncClient() as client:
            latestVersion = await client.get(
                "https://api.github.com/repos/sigma67/ytmusicapi/release", timeout=None
            )
        latestVersion = latestVersion.json()[0]["tag_name"]

        global MUSICAPI_VERSION
        updated = latestVersion == MUSICAPI_VERSION
        print(f"[update] Installed ytmusicapi version  : {MUSICAPI_VERSION}.")
        print(f"[update] Latest ytmusicapi Version     : {latestVersion}.")
        if not updated:
            print("[update] Updating ytmusicapi...")
            cmd = f"{sys.executable} -m pip install --upgrade git+https://github.com/sigma67/ytmusicapi@master"

            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            while process.poll() is None:
                await asyncio.sleep(0.1)
            stdout, stderr = process.communicate()
            stdout, stderr = stdout.decode(), stderr.decode()
            if process.poll() == 0:
                MUSICAPI_VERSION = latestVersion
                print(f"[update] Updated To ytmusicapi version : {latestVersion}")
            else:
                print("[update] Failed to update.")
                print("[stdout]", stdout)
                print("[stderr]", stderr)
        else:
            print("[update] ytmusicapi is already updated.")
