from typing import List, Union

import httpx
import os
import aiofiles
from youtubesearchpython.__future__ import VideosSearch


def getValue(source: dict, path: List[str]) -> Union[str, int, dict, None]:
    value = source
    for key in path:
        if type(key) is str:
            if key in value.keys():
                value = value[key]
            else:
                value = None
                break
        elif type(key) is int:
            if len(value) != 0:
                value = value[key]
            else:
                value = None
                break
    return value

class Video:
    @staticmethod
    def getFormat(videoId: str) -> dict:
        player = httpx.post(
            "https://www.youtube.com/youtubei/v1/player",
            json={
                "context": {
                    "client": {
                        "clientName": "ANDROID",
                        "clientScreen": "EMBED",
                        "clientVersion": "16.43.34",
                    },
                    "thirdParty": {
                        "embedUrl": "https://www.youtube.com",
                    },
                },
                "videoId": videoId,
            },
            headers={"X-Goog-Api-Key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"}
        ).json()

        component = {
            'id': getValue(player, ['videoDetails', 'videoId']),
            'title': getValue(player, ['videoDetails', 'title']),
            'duration': {
                'secondsText': getValue(player, ['videoDetails', 'lengthSeconds']),
            },
            'viewCount': {
                'text': getValue(player, ['videoDetails', 'viewCount'])
            },
            'thumbnails': getValue(player, ['videoDetails', 'thumbnail', 'thumbnails']),
            'description': getValue(player, ['videoDetails', 'shortDescription']),
            'channel': {
                'name': getValue(player, ['videoDetails', 'author']),
                'id': getValue(player, ['videoDetails', 'channelId']),
            },
            'allowRatings': getValue(player, ['videoDetails', 'allowRatings']),
            'averageRating': getValue(player, ['videoDetails', 'averageRating']),
            'keywords': getValue(player, ['videoDetails', 'keywords']),
            'isLiveContent': getValue(player, ['videoDetails', 'isLiveContent']),
            'publishDate': getValue(player, ['microformat', 'playerMicroformatRenderer', 'publishDate']),
            'uploadDate': getValue(player, ['microformat', 'playerMicroformatRenderer', 'uploadDate']),
        }
        component['isLiveNow'] = component['isLiveContent'] and component['duration']['secondsText'] == "0"
        component['link'] = 'https://www.youtube.com/watch?v=' + component['id']
        component['channel']['link'] = 'https://www.youtube.com/channel/' + component['channel']['id']

        formats = player["streamingData"]["adaptiveFormats"]
        for f in formats:
            if f["itag"] == 251:
                component["url"] = f["url"]
            elif f["itag"] == 140:
                # Fallback aac
                component["fallbackURL"] = f["url"]
        return component

class YouTube:
    def __init__(self):
        pass

    async def download(self, videoName: str) -> dict:
        if 'youtu' not in videoName:
            ''' Searching Video '''
            video = await self.__getVideo(videoName)
            if not video:
                return None
            videoId = video['id']
        else:
            videoId = self.__getVideoId(videoName)
        ''' Getting Stream URL '''
        video = Video.getFormat(videoId)
        videoUrl = video["url"]
        if not videoUrl:
            ''' Fallback AAC '''
            videoUrl = video["fallbackURL"]
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
            
    def __getVideoId(self, videoLink: str) -> str:
        if 'youtu.be' in videoLink:
            if videoLink[-1] == '/':
                return videoLink.split('/')[-2]
            return videoLink.split('/')[-1]
        elif 'youtube.com' in videoLink:
            if '&' not in videoLink:
                return videoLink[videoLink.index('v=') + 2:]
            return videoLink[videoLink.index('v=') + 2: videoLink.index('&')]
        else:
            return videoLink

    async def __getVideo(self, videoName):
        search = VideosSearch(videoName, limit=1)
        result = await search.next()
        return result['result'][0]
