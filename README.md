# harmonoid-bot
[WIP] Harmonoid bot for Discord, that plays your favorite music and can even download it!

## [Add me to your server](https://discord.com/oauth2/authorize?client_id=802600265005137980&scope=bot&permissions=36932608)


# Commands
| Command                 | Aliases             | What does it do                                                                           |
|-------------------------|---------------------|-------------------------------------------------------------------------------------------|
| !play <song name>       | !p                  | Joins a voice channel called Music, and plays the song from Youtube Music                 |
| !playYT <song name>     | !play_yt !py        | Joins a voice channel called Music, and plays the song or video (only audio) from YouTube |
| !stop                   | !s                  | Stops playing a song                                                                      |
| !pause                  |                     | Pauses playing a song                                                                     |
| !resume                 | !r                  | Resumes playing a song                                                                    |
| !lyrics <song name>     |                     | Sends lyrics of the song into the chat if he finds them                                   |
| !lyricsSend <song name> |                     | Sends lyrics of the song into the chat in .txt document if he finds them                  |
| !disconnect             |                     | Disconnects from a voice channel                                                          |
| !about                  |                     | Send about embed into chat                                                                |
| !playQueue <song name>  | !pq !add !queue add | Adds specific song from YouTube to queue                                                  |
| !queue                  | !q                  | Shows current queue for server                                                            |
| !remove                 | !rm                 | Remove specific song position from queue                                                  |
| !clear                  | !qc !cl             | Clears current queue                                                                      |

# Commands in beta
- !about
- !pq <song name>
- !q
- !clear
- !remove

# Features in beta
- Auto-disconnect every 10 minutes on empty channel
- Queue

# :heart: Special thanks to this people & organisations
- [harmonoid](https://github.com/harmonoid) for [harmonoid-service](https://github.com/harmonoid/harmonoid-service)
- [sigmatics](https://github.com/sigma67) for [ytmusicapi](https://github.com/sigma67/ytmusicapi)
- [PyTube](https://github.com/pytube) for [PyTube](https://github.com/pytube/pytube)
- [Quod Libet](https://github.com/quodlibet) for [mutagen](https://github.com/quodlibet/mutagen)
- [Encode](https://github.com/encode) for [httpx](https://github.com/encode/httpx)
- [Tin Tvrtković](https://github.com/Tinche) for [aiofiles](https://github.com/Tinche/aiofiles)
- [alexmercerind](https://github.com/alexmercerind) for [youtube-search-python](https://github.com/alexmercerind/youtube-search-python)
- [Danny](https://github.com/Rapptz) for [discord.py](https://github.com/Rapptz/discord.py)

<!--
# News
We removed auto-disconnect, since during testing, it crashed a server
-->
