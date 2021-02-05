from commands import *


class Controls(Commands):

    def __init__(self):
        super().__init__(Commands.bot)

    @commands.command(aliases=['pp'])
    async def togglePlayback(self, ctx):
        if not (server := await Server.get(ctx)):
            return None
        if server.voiceConnection:
            if server.voiceConnection.is_playing():
                server.pause()
                await self.embed.text(
                    ctx,
                    'Paused Music. ⏸',
                    '✅'
                )
            else:
                server.resume()
                await self.embed.text(
                    ctx,
                    'Resumed Music. ▶',
                    '✅'
                )
        else:
            await self.embed.text(
                ctx,
                'Nothing is playing. ❌',
                '❌'
            )