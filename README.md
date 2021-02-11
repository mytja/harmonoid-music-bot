# harmonoid-music-bot
Harmonoid bot for Discord, that plays your favorite music, manages queue, sends lyrics, and much more...

# [Test me on Harmonoid's Discord server](https://discord.gg/mRxH9zYkGy/)

## [Add me to your server](https://discord.com/oauth2/authorize?client_id=802600265005137980&scope=bot&permissions=36932608)

# Deploying it yourself
Please note, that link for adding it to server is strictly intended for personal & non-commercial use. You are responsible for any non-intended & not-legal usage of this bot and/or server.

You can deploy it to Heroku or a self hosted machine.

## Deploying to Heroku
1. Create an account on Heroku if you don't have it yet
2. Create an app
3. Create a fork of our repo on GitHub & Deploy it on Heroku
4. Get a Discord Bot Token from Discord
5. Add a secret key called DISCORD_TOKEN with value of a discord token, you got earlier, to Heroku app
6. Flip a toggle switch on main page of your app

# Playing commands
| Command                 | Aliases             | What does it do                                                                           |
|-------------------------|---------------------|-------------------------------------------------------------------------------------------|
| -play <song name>       | -p                  | Adds a track from YouTube Music to queue                                                  |
| -playYT <song name>     | -py                 | Adds a track from YouTube to queue                                                        |
| -togglePlayback         | -pp                 | Pauses or resumes playing song, depending on if song is playing                           |

# Queue commands
| Command                 | Aliases             | What does it do                                                                           |
|-------------------------|---------------------|-------------------------------------------------------------------------------------------|
| -queue                  | -q                  | Displays a current queue                                                                  |
| -next                   | -n                  | Jumps onto next song in queue                                                             |
| -back                   | -b                  | Jumps one song back on queue                                                              |
| -jump <song ID>         | -j                  | Jumps onto a song ID you gave in the command in the queue                                 |
| -delete <song ID>       | -d                  | Deletes a song with ID you gave in the command from queue                                 |
| -clear                  | -c                  | Clears current queue                                                                      |

# General commands
| Command                          | Aliases             | What does it do                                                                           |
|----------------------------------|---------------------|-------------------------------------------------------------------------------------------|
| -status                          | -s                  | Displays server status/statistics                                                         |
| -about                           | -a                  | Displays an about dialog                                                                  |
| -lyrics <song name>              |                     | Sends lyrics of the song into the chat if he finds them                                   |
| -lyricsSend <song name>          |                     | Sends lyrics of the song into the chat in .txt document if he finds them                  |
| -confvcname <voice channel name> | -cvcname            | Changes Voice Channel in which it plays music                                             |

# :heart: Special thanks to this people & organisations
- [sigmatics](https://github.com/sigma67) for [ytmusicapi](https://github.com/sigma67/ytmusicapi)
- [PyTube](https://github.com/pytube) for [PyTube](https://github.com/pytube/pytube)
- [Encode](https://github.com/encode) for [httpx](https://github.com/encode/httpx)
- [Tin Tvrtković](https://github.com/Tinche) for [aiofiles](https://github.com/Tinche/aiofiles)
- [alexmercerind](https://github.com/alexmercerind) for [youtube-search-python](https://github.com/alexmercerind/youtube-search-python)
- [Danny](https://github.com/Rapptz) for [discord.py](https://github.com/Rapptz/discord.py)
