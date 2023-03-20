from youtubesearchpython.__future__ import VideosSearch, Video, StreamURLFetcher

from typing import List, Union


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

class YouTube:
    def __init__(self):
        self.fetcher = StreamURLFetcher()
        pass

    async def init_fetcher(self):
        await self.fetcher.getJavaScript()


    async def fetch_url(self, video, url):
        if "url" in video.keys():
            return video["url"]
        return await self.fetcher.get(video, url)

    async def download(self, videoName: str) -> dict:
        if 'youtu' not in videoName:
            video = await self.__getVideo(videoName)
            if not video:
                return None
            videoId = video['id']
        else:
            videoId = self.__getVideoId(videoName)
        video = await Video.get(videoId)
        print(video)
        return video
            
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


youtube = YouTube()
