import discord

async def embedNowYT(music, ctx):
    embed=discord.Embed(title="Now playing:", description=f"**[{music['title']}]({music['url']})**", color=discord.Colour.random())
    embed.set_thumbnail(url=music["thumbnail"])
    embed.add_field(name="Requested by:", value=f"`{ctx.author.name}`", inline=True)
    embed.add_field(name="Duration:", value=f"`{music['duration']}`", inline=True)
    await ctx.send(embed=embed)

async def embedNow(music, ctx):
    trackDur = music["trackDuration"]
    url = "https://music.youtube.com/watch?v="+music["trackId"]
                    
    embed=discord.Embed(title="Now playing :", description=f"**[{music['trackName']}]({url})**", color=discord.Colour.random())
    embed.set_thumbnail(url=music["albumArtHigh"])
    embed.add_field(name="Requested by :", value=f"`{ctx.author.name}`", inline=True)
    embed.add_field(name="Duration :", value=f"`{trackDur//60}:{trackDur%60}`", inline=True)
    
    embed.add_field(name="Album name :", value=f"`{music['albumName']}`", inline=True)
    embed.add_field(name="Year :", value=f"`{music['year']}`", inline=True)
    
    embed.add_field(name="Artists :", value=f"`{', '.join(music['trackArtistNames'])}`", inline=True)
    
    
    await ctx.send(embed=embed)

async def embedAbout(ctx):
    about = """
    Hello! :wave:
    I'm Harmonoid Bot. 
    I can play music for you, download lyrics, and everything for free. :tada: 
    I'm still in development phase, so please report any problems. You should get an error ID with error. Report a problem with an error ID 
    Sometimes, I can't find some songs. That's because my backend was rewrited a lot of times for improving preformance, and is still a little buggy 
    Please don't download songs longer than 10 minutes, otherwise you will probably have to wait a long time, before it is going to play. 
    I'm strictly intended for personal & non-commercial usage. 
    Thanks for using me in your server. 
    You won't regret it :wink: ! 
    - harmonoid Team
    """

    version = "Beta 1.0.0"

    maintainers = "mytja, alexmercerind, raitonoberu"
                    
    embed=discord.Embed(title="About:", description="**About harmonoid-bot**", color=discord.Colour.random())
    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/75374037?s=200&v=4")
    embed.add_field(name='About: ', value=f"{about}", inline=False)
    embed.add_field(name="Version: ", value=f"{version}", inline=True)
    embed.add_field(name="Maintainers: ", value=f"{maintainers}", inline=True)
    
    
    await ctx.send(embed=embed)

async def reallyDownloadEmbed(music):
    embed=discord.Embed(title="Do you want to download it?:", description=f"**[{music['title']}]({music['url']})**", color=discord.Colour.random())
    embed.set_thumbnail(url=music["thumbnail"])
    embed.add_field(name="Requested by:", value=f"`{music['author']}`", inline=True)
    embed.add_field(name="Duration:", value=f"`{music['duration']}`", inline=True)
    return embed