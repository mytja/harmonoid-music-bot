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

    async def getLyrics(self, trackName, save = False):
        result = await self.__youtube.searchYouTube(trackName, 'songs')
        track = result[0]
        watchPlaylist = await self.__youtube.getWatchPlaylist(track['videoId'])
        try:
            lyrics = await self.__youtube.getLyrics(watchPlaylist['lyrics'])
            if save:
                async with aiofiles.open('lyrics.txt', 'w', encoding='utf_8') as file:
                    await file.write(lyrics['lyrics'])
            lyrics.update(track)
            return lyrics
        except:
            return None
    
    def __getTrackId(self, trackLink: str) -> str:
        if '&' not in trackLink:
            return trackLink[trackLink.index('v=') + 2:]
        else:
            return trackLink[trackLink.index('v=') + 2: trackLink.index('&')]

    async def __getTrack(self, trackName):
        if 'music.youtube' not in trackName:
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
        else:
            trackId = self.__getTrackId(trackName)
            track = await self.__youtube.getSong(trackId)
            albumResult = await self.__youtube.searchYouTube(track['title'], 'songs')
            album = albumResult[0]
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
                'albumName': album['album']['name'],
                'year': track['release'].split('-')[0],
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
