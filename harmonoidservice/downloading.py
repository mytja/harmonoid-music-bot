import httpx
import subprocess
import aiofiles
import aiofiles.os
import os
import sys
import asyncio
import json
import ytmusicapi
from pytube import YouTube
from .async_mutagen import Metadata
from youtubesearchpython.__future__ import *

fetcher = StreamURLFetcher()

MUSICAPI_VERSION = ytmusicapi.__version__
FFMPEG_COMMAND = 'ffmpeg -i {trackId}.webm -vn -c:a copy {trackId}.ogg'


class DownloadHandler:
    async def trackDownload(self, trackId, albumId, trackName):
        if trackId:
            print(f"[server] Download request in ID format.")
        if trackName:
            print(f"[server] Download request in name format.")
            result = await self.ytMusic.searchYoutube(trackName, "songs")
            trackId = result[0]["videoId"]
            albumId = result[0]["album"]["id"]
        

        trackInfo = await self.trackInfo(trackId, albumId)
        print(trackInfo)
        
        if os.path.isfile(f"{trackId}.ogg"):
            print(
                f"[pytube] Track already downloaded for track ID: {trackId}.\n[server] Sending audio binary for track ID: {trackId}."
            )
            return trackInfo
        
        
        if type(trackInfo) is dict:
            print(
                f"[ytmusicapi] Successfully retrieved metadata of track ID: {trackId}."
            )
            await self.saveAudio(trackInfo, metadataAdd=True)
            print(f"[server] Sending audio binary for track ID: {trackId}")
            return trackInfo
        else:
            print(f"[ytmusicapi] Could not retrieve metadata of track ID: {trackId}.")
            print(f"[server] Sending status code 500 for track ID: {trackId}.")
            return None

    async def YTdownload(self, trackName):
        await fetcher.getJavaScript()
        if trackName:
            print(f"[server] Download request in name format.")
            try:
                result = await self.browsingHandler.searchYT(trackName)
                result = result["result"][0]
            except Exception as e:
                print(f"[track-search] {e}")
                return
        
        url = "https://youtube.com/watch?v="+result["id"]
        
        trackId = result["id"]
        
        title = result["title"]
        #title = title.replace("`", "")
        #title = title.replace("´", "")
        title = title.replace("'", "")
        title = title.replace('"', "")
        print(title)
        
        video = await Video.get(url)
        furl = await fetcher.get(video, 251)
        
        trackInfo = {
            "trackId": trackId,
            "url": url,
            "filename": trackId+".ogg",
            "thumbnail": result["thumbnails"][0]["url"],
            "duration": result["duration"],
            "opusTrackName": trackId+".webm",
            "title": title,
            "fURL": furl
        }
        print(trackInfo)
        
        
        if os.path.isfile(f"{trackId}.ogg"):
            print(
                f"[pytube] Track already downloaded for track ID: {trackId}.\n[server] Sending audio binary for track ID: {trackId}."
            )
            return trackInfo
            
        
        try:
            await self.saveAudio(trackInfo, metadataAdd=False)
        except Exception as e:
            print(f"[save-audio] {e}")

        print(f"[server] Sending audio binary for track ID: {trackId}")
        return trackInfo

    async def saveAudio(self, trackInfo, metadataAdd):
        filename = f"{trackInfo['trackId']}.webm"
        print(f"[httpx] Downloading track ID: {trackInfo['trackId']}.")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                trackInfo["fURL"], timeout=None, headers={"Range": "bytes=0-"}
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

