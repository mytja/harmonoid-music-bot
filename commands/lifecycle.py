from commands import *


class Lifecycle:
    @staticmethod
    async def listen():
        while True:
            await Commands.bot.wait_until_ready()
            for server in Commands.recognisedServers:
                try:
                    if not server.voiceConnection.is_playing() and server.queue:
                        ''' Playing Track '''
                        track = server.queue[0]
                        voiceChannel = await server.getVoiceChannel(server.context)
                        try:
                            voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
                        except:
                            try:
                                voiceChannel.stop()
                                voiceChannel.play(discord.FFmpegOpusAudio(f'{track["trackId"]}.webm'))
                            except:
                                await Embed().exception(
                                    server.context,
                                    'Internal Error',
                                    f'Could not start player. 📻',
                                    '❌'
                                )
                                return None
                        ''' Displaying Metadata '''
                        try:
                            await Embed().nowPlaying(server.context, track)
                        except:
                            await Embed().exception(
                                server.context,
                                'Now Playing',
                                'Could not send track information.\nMusic is still playing. 👌',
                                '👌'
                            )
                        server.queue.pop(0)
                except:
                    pass
            await asyncio.sleep(5)