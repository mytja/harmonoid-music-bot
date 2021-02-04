import httpx
import os
import aiofiles
import asyncio
from scripts.internal import YTM


class YouTubeMusic:
    def __init__(self):
        self.__youtube = YTM()

    async def download(self, trackName: str) -> dict:
        ''' Searching Track '''
        track = await self.__getTrack(trackName)
        if not track:
            return None
        trackId = track['trackId']
        ''' Getting Stream URL '''
        trackUrl = track['url']
        if os.path.isfile(f'{trackId}.webm'):
            return track
        elif type(track) is dict:
            ''' Saving Track File '''
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    trackUrl,
                    timeout=None,
                    headers={'Range': 'bytes=0-'}
                )
            if response.status_code in [200, 206]:
                async with aiofiles.open(f'{trackId}.webm', 'wb') as file:
                    await file.write(response.content)
            return track
        else:
            return None

    async def __getTrack(self, trackName):
        result = await self.__youtube.searchYouTube(trackName, 'songs')
        track, album = await asyncio.gather(
            self.__youtube.getSong(result[0]['videoId']),
            self.__youtube.getAlbum(result[0]['album']['id']),
        )
        albumArtLow, albumArtMedium, albumArtHigh = self.__sortThumbnails(
            album['thumbnails']
        )
        return {
            'trackId': track['videoId'],
            'trackName': track['title'],
            'trackArtistNames': [artist for artist in track['artists']],
            'trackDuration': track['lengthSeconds'],
            'albumArtHigh': albumArtHigh,
            'albumArtMedium': albumArtMedium,
            'albumArtLow': albumArtLow,
            'albumName': album['title'],
            'year': album['releaseDate']['year'],
            'url': track['url'],
        }

    def __sortThumbnails(self, thumbnails):
        thumbs = {}
        for thumbnail in thumbnails:
            wh = thumbnail['width'] * thumbnail['height']
            thumbs[wh] = thumbnail['url']
        resolutions = sorted(list(thumbs.keys()))
        max = resolutions[-1]
        mid = resolutions[-2] if len(resolutions) > 2 else max
        min = resolutions[0]
        return (thumbs[min], thumbs[mid], thumbs[max])
