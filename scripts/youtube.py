import httpx
import os
import aiofiles
from youtubesearchpython.__future__ import Video, VideosSearch, StreamURLFetcher


class YouTube:
    def __init__(self):
        self.streamURL = StreamURLFetcher()

    async def download(self, videoName: str) -> dict:
        ''' Searching Video '''
        video = await self.__getVideo(videoName)
        if not video:
            return None
        videoId = video['id']
        ''' Getting Stream URL '''
        video = await Video.get(videoId)
        videoUrl = await self.streamURL.get(video, 251)
        if not videoUrl:
            ''' Fallback AAC '''
            videoUrl = await self.streamURL.get(video, 140)
        if os.path.isfile(f'{videoId}.webm'):
            return video
        elif type(video) is dict:
            ''' Saving Track File '''
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    videoUrl,
                    timeout=None,
                    headers={'Range': 'bytes=0-'}
                )
            if response.status_code in [200, 206]:
                async with aiofiles.open(f'{videoId}.webm', 'wb') as file:
                    await file.write(response.content)
            return video
        else:
            return None

    async def __getVideo(self, videoName):
        search = VideosSearch(videoName, limit=1)
        result = await search.next()
        return result['result'][0]