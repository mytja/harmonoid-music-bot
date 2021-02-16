<h1 align='center'><a href='https://github.com/harmonoid/harmonoid-music-bot'>Harmonoid Music Bot</a></h1>
<h4 align='center'>🎵 Music bot for Discord. Supports lyrics, queues & plays using both YT Music & YouTube.</h4>
<p align='center'><a href='https://discord.com/oauth2/authorize?client_id=802600265005137980&scope=bot&permissions=36932608'>Invite</a> | <a href='https://discord.com/invite/ZG7Pj9SREG'>Discord</a> | <a href='https://harmonoid.github.io/harmonoid-music-bot'>Website</a></p>

<table>
  <tr>
    <td><img src='https://github.com/harmonoid/harmonoid-music-bot/blob/screenshots/1.PNG?raw=true'></img></td>
    <td><img src='https://github.com/harmonoid/harmonoid-music-bot/blob/screenshots/2.PNG?raw=true'></img></td>
    <td><img src='https://github.com/harmonoid/harmonoid-music-bot/blob/screenshots/3.PNG?raw=true'></img></td>
  </tr>
</table>

## 💜 Support

You may join our [Discord](https://discord.com/invite/ZG7Pj9SREG) server to provide feedback, report bugs in the bot or just chill.

## 🎵 Invite

To use me in your server, use [this](https://discord.com/oauth2/authorize?client_id=802600265005137980&scope=bot&permissions=36932608) link to invite me.

## 🎹 Commands

### 🎵 Playback Commands

| Command                     | Aliases  | Action                                                                                    |
|-----------------------------|----------|-------------------------------------------------------------------------------------------|
| -play   <song name or link> | -p       | Plays or adds a track to queue from YouTube Music.                                        |
| -playYT <song name or link> | -py      | Plays or adds a track to queue from YouTube.                                              |
| -pause                      |          | Pauses playback.                                                                          |
| -resume                     |          | Resumes playback.                                                                         |
| -togglePlayback             | -pp      | Switches between pause & play states.                                                     |

### 📑 Queue Commands

| Command                 | Aliases  | Action                                                                                    |
|-------------------------|----------|-------------------------------------------------------------------------------------------|
| -queue                  | -q       | Displays the current queue.                                                               |
| -next                   | -n       | Jumps to next track in the queue.                                                         |
| -back                   | -b       | Jumps to previous track in the queue.                                                     |
| -jump   <position>      | -j       | Jumps to specific track in the queue based on its position.                               |
| -delete <position>      | -d       | Removes track from the queue from the given position.                                     |
| -clear                  | -c       | Clears the queue.                                                                         |
  
### 🧰 Utility Commands

| Command                             | Aliases  | Action                                                                                    |
|-------------------------------------|----------|-------------------------------------------------------------------------------------------|
| -lyrics     <song name>             | -l       | Shows lyrics of a track.                                                                  |
| -lyricsSend <song name>             | -ls      | Sends lyrics of a track in a TXT file.                                                    |
| -changeChannel <voice channel name> | -cc      | Changes voice channel where music should be played.                                       |

### 📖 Other Commands

| Command                             | Aliases  | Action                                                                                    |
|-------------------------------------|----------|-------------------------------------------------------------------------------------------|
| -status                             | -s       | Displays bot's statistics.                                                                |
| -about                              | -a       | Displays information about bot.                                                           |

## 🔐 Deploy Personally

You can deploy this bot on Heroku or on a self hosted machine.

#### Deploying to Heroku
- Create an account on Heroku if you don't have it yet
- Create an app
- Create a fork of our repo on GitHub & Deploy it on Heroku
- Get a Discord Bot Token from Discord
- Add a secret key called DISCORD_TOKEN with value of a discord token, you got earlier, to Heroku app
- Flip a toggle switch on main page of your app

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## ⭐ Acknowledgements
- [sigmatics](https://github.com/sigma67) for [ytmusicapi](https://github.com/sigma67/ytmusicapi)
- [PyTube](https://github.com/pytube) for [PyTube](https://github.com/pytube/pytube)
- [Encode](https://github.com/encode) for [httpx](https://github.com/encode/httpx)
- [Tin Tvrtković](https://github.com/Tinche) for [aiofiles](https://github.com/Tinche/aiofiles)
- [alexmercerind](https://github.com/alexmercerind) for [youtube-search-python](https://github.com/alexmercerind/youtube-search-python)
- [Danny](https://github.com/Rapptz) for [discord.py](https://github.com/Rapptz/discord.py)
