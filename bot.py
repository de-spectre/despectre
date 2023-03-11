import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands

import mafic

import config


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pool = mafic.NodePool(self)
        self.loop.create_task(self.add_nodes())

    async def add_nodes(self):
        await self.pool.create_node(
            host="127.0.0.1",
            port='2333',
            label="MAIN",
            password="youshallnotpass",
        )


client = MyBot(intents=nextcord.Intents(guilds=True, voice_states=True))



@client.event
async def on_ready():
    print(f'{client.user} started!')


# 
# 
#  COMMANDS
# 
# 






# 
# 
#   MUSIC
# 
# 



@client.slash_command(dm_permission=False, name='play', description='Play music')
async def play(inter: nextcord.Interaction, query: str = SlashOption(name='search', description='Music to play', required=True)):
    if not inter.guild.voice_client:
        player = await inter.user.voice.channel.connect(cls=mafic.Player)
    else:
        player = inter.guild.voice_client

    tracks = await player.fetch_tracks(query)

    if not tracks:
        return await inter.send("No tracks found.")

    track = tracks[0]

    embed  = nextcord.Embed(title=f'{track.title}', color=config.BASE_COLOR)
    embed.set_author(name='Now playing:')


    await player.play(track)

    await inter.send(embed=embed)


@client.slash_command(name='leave', description='Leave voice channel')
async def leave_cmd(inter: Interaction):
    vc = inter.guild.voice_client

    await vc.disconnect()
    await inter.send('Disconnected')







client.run(config.TOKEN)