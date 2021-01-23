import asyncio


class BrowsingHandlerInternal:
    async def arrangeVideoIds(self, track):
        title = track["artists"] + " " + track["title"]
        youtubeResult = await self.ytMusic.searchYoutube(title, "songs")
        if track["title"] in youtubeResult[0]["title"]:
            return youtubeResult[0]["videoId"]
        else:
            return track["videoId"]

    async def asyncAlbumSearch(self, tracks):
        tasks = [self.arrangeVideoIds(track) for track in tracks]
        return await asyncio.gather(*tasks)
    
    def sortThumbnails(self, thumbnails):
        thumbs = {}
        for thumbnail in thumbnails:
            wh = thumbnail["width"] * thumbnail["height"]
            thumbs[wh] = thumbnail["url"]
        resolutions = sorted(list(thumbs.keys()))
        max = resolutions[-1]
        mid = resolutions[-2] if len(resolutions) > 2 else max
        min = resolutions[0]

        return (thumbs[min], thumbs[mid], thumbs[max])
    
    """
    Commented out code, which was used for fetching missing keys in <=0.0.2+2 version of app.
    """
    """
    async def arrangeAlbumLength(self, album):
        youtubeResult = await self.ytMusic.getAlbum(album["browseId"])
        return int(youtubeResult["trackCount"])

    async def asyncAlbumLength(self, albums):
        tasks = [self.arrangeAlbumLength(album) for album in albums]
        return await asyncio.gather(*tasks)

    async def arrangeTrackDuration(self, track):
        trackInfo = await self.ytMusic.getSong(track["videoId"])
        return int(trackInfo["lengthSeconds"])

    async def asyncTrackDuration(self, tracks):
        tasks = [self.arrangeTrackDuration(track) for track in tracks]
        return await asyncio.gather(*tasks)
    
    async def arrangeTrackStuff(self, track):
        if track["album"] != None:
            youtubeResult = await self.ytMusic.getAlbum(track["album"]["id"])
            for result_track in youtubeResult["tracks"]:
                if result_track["title"] == track["title"]:
                    number = int(result_track["index"])
                    break
            year = youtubeResult["releaseDate"]["year"]
            artists = [a["name"] for a in youtubeResult["artist"]]
            length = int(youtubeResult["trackCount"])
            type = "single" if len(youtubeResult["tracks"]) == 1 else "album"
            return (number, year, artists, length, type)

    async def asyncTrackStuff(self, tracks):
        tasks = [self.arrangeTrackStuff(track) for track in tracks]
        return await asyncio.gather(*tasks)
    """


class BrowsingHandler(BrowsingHandlerInternal):
    async def trackInfo(self, trackId, albumId):
        if trackId and albumId:
            """
            Making simultaneous request if both albumId & trackId are present.
            """
            track, album = await asyncio.gather(self.ytMusic.getSong(trackId), self.ytMusic.getAlbum(albumId))
        else:
            track = await self.ytMusic.getSong(trackId)
            """
            Searching for track & fetching albumId if it is None.
            """
            albumId = await self.ytMusic.searchYoutube(
                " ".join([artist for artist in track["artists"]]) + " " + track["title"], "songs"
            )
            albumId = albumId[0]["album"]["id"]
            album = await self.ytMusic.getAlbum(albumId)
        trackNumber = 1
        albumArtLow, albumArtMedium, albumArtHigh = self.sortThumbnails(
            album["thumbnails"]
        )
        for albumTrack in album["tracks"]:
            if albumTrack["title"] == track["title"]:
                trackNumber = int(albumTrack["index"])
                break
        albumArtistName = [a["name"] for a in album["artist"]]
        return {
            "trackId": track["videoId"],
            "trackName": track["title"],
            "trackArtistNames": [artist for artist in track["artists"]],
            "trackNumber": trackNumber,
            "trackDuration": int(track["lengthSeconds"]) if track["lengthSeconds"] else 0,
            "albumArtHigh": albumArtHigh,
            "albumArtMedium": albumArtMedium,
            "albumArtLow": albumArtLow,
            "albumId": albumId,
            "albumName": album["title"],
            "year": album["releaseDate"]["year"],
            "albumArtistName": albumArtistName[0],
            "albumLength": int(album["trackCount"]),
            "albumType": "single" if len(album["tracks"]) == 1 else "album",
            "url": track["url"],
        }

    async def albumInfo(self, albumId):
        response = await self.ytMusic.getAlbum(albumId)
        tracks = response["tracks"]
        """
        For replacing video IDs of music videos with video IDs of tracks.
        """
        videoIdList = await self.asyncAlbumSearch(tracks)
        result = []
        for index, track in enumerate(tracks):
            result += [
                {
                    "trackId": videoIdList[index],
                    "trackName": track["title"],
                    "trackArtistNames": [track["artists"]],
                    "trackNumber": int(track["index"]),
                    "trackDuration": int(track["lengthMs"]) // 1000 if track["lengthMs"] else 0,
                }
            ]
        return {"tracks": result}

    async def artistAlbums(self, artistId):
        artistJson = await self.ytMusic.getArtist(artistId)
        albums = artistJson["albums"]["results"] + artistJson["singles"]["results"]
        artistAlbums = []
        for album in albums:
            albumArtLow, albumArtMedium, albumArtHigh = self.sortThumbnails(
                album["thumbnails"]
            )
            artistAlbums += [
                {
                    "albumId": album["browseId"],
                    "albumName": album["title"],
                    "year": album["year"],
                    "albumArtistName": [artistJson["name"]][0],
                    "albumArtHigh": albumArtHigh,
                    "albumArtMedium": albumArtMedium,
                    "albumArtLow": albumArtLow,
                }
            ]
        return {"albums": artistAlbums}

    async def artistTracks(self, artistId):
        artistJson = await self.ytMusic.getArtist(artistId)
        tracks = artistJson["songs"]["results"]
        artistTracks = []
        for track in tracks:
            trackArtistNames = [a["name"] for a in track["artists"]]
            albumArtLow, albumArtMedium, albumArtHigh = self.sortThumbnails(
                track["thumbnails"]
            )
            artistTracks += [
                {
                    "trackId": track["videoId"],
                    "trackName": track["title"],
                    "trackArtistNames": trackArtistNames,
                    "albumArtHigh": albumArtHigh,
                    "albumArtMedium": albumArtMedium,
                    "albumArtLow": albumArtLow,
                    "albumId": track["album"]["id"],
                    "albumName": track["album"]["name"],
                }
            ]
        return {"tracks": artistTracks}

    async def artistInfo(self, artistId):
        artistJson = await self.ytMusic.getArtist(artistId)
        return {
            "description": artistJson["description"],
            "subscribers": artistJson["subscribers"],
            "views": artistJson["views"],
        }

    async def searchYoutube(self, keyword, mode):
        if mode == "album":
            youtubeResult = await self.ytMusic.searchYoutube(keyword, "albums")
            albums = []
            for album in youtubeResult:
                albumArtLow, albumArtMedium, albumArtHigh = self.sortThumbnails(
                    album["thumbnails"]
                )
                albums += [
                    {
                        "albumId": album["browseId"],
                        "albumName": album["title"],
                        "year": int(album["year"]) if album["year"] and album["year"].isnumeric() else 0,
                        "albumArtistName": album["artist"],
                        "albumArtHigh": albumArtHigh,
                        "albumArtMedium": albumArtMedium,
                        "albumArtLow": albumArtLow,
                    }
                ]
            return {"result": albums}

        if mode == "track":
            youtubeResult = await self.ytMusic.searchYoutube(keyword, "songs")
            tracks = []
            for track in youtubeResult:
                if track["album"] != None:
                    albumArtLow, albumArtMedium, albumArtHigh = self.sortThumbnails(
                        track["thumbnails"]
                    )
                    trackArtistNames = [a["name"] for a in track["artists"]]
                    tracks += [
                        {
                            "trackId": track["videoId"],
                            "trackName": track["title"],
                            "trackArtistNames": trackArtistNames,
                            "trackDuration": (
                                int(track["duration"].split(":")[0]) * 60
                                + int(track["duration"].split(":")[-1])
                            ),
                            "albumId": track["album"]["id"],
                            "albumName": track["album"]["name"],
                            "albumArtHigh": albumArtHigh,
                            "albumArtMedium": albumArtMedium,
                            "albumArtLow": albumArtLow,
                        }
                    ]
            return {"result": tracks}

        if mode == "artist":
            youtubeResult = await self.ytMusic.searchYoutube(keyword, "artists")

            artists = []
            for artist in youtubeResult:
                albumArtLow, albumArtMedium, albumArtHigh = self.sortThumbnails(
                    artist["thumbnails"]
                )
                artists += [
                    {
                        "artistId": artist["browseId"],
                        "artistName": artist["artist"],
                        "artistArtHigh": albumArtHigh,
                        "artistArtMedium": albumArtMedium,
                        "artistArtLow": albumArtLow,
                    }
                ]
            return {"result": artists}

    async def getLyrics(self, trackId, trackName):
        if not trackId:
            trackId = (await self.searchYoutube(trackName, "track"))["result"][0]["trackId"]
        watchPlaylist = await self.ytMusic.getWatchPlaylist(trackId)
        watchPlaylistId = watchPlaylist["lyrics"]
        return await self.ytMusic.getLyrics(watchPlaylistId)
