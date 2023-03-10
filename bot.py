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


@client.slash_command(name='help', description='All commands')
async def help_cmd(inter: Interaction):

    embed=nextcord.Embed(title="All commands", color=0xb6ace3)
    embed.set_author(name="[beta]")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/1058143525004390401/346701886fb5ff9902243c6ff4145496.png?size=1024")
    embed.add_field(name="/help", value="Shows this list", inline=True)
    embed.add_field(name="/stats [member]", value="User info", inline=True)

    await inter.send(embed=embed)

@client.slash_command(name='stats', description='Shows member stats')
async def stats_cmd(inter: Interaction, member: nextcord.User):
    embed=nextcord.Embed(title=f"{member.display_name}", description="", color=0xb6ace3)
    embed.set_thumbnail(url=f"{member.avatar.url}")
    await inter.send(embed=embed)



# 
# 
#   MUSIC
# 
# 



@client.slash_command(dm_permission=False)
async def play(inter: nextcord.Interaction, query: str):
    if not inter.guild.voice_client:
        player = await inter.user.voice.channel.connect(cls=mafic.Player)
    else:
        player = inter.guild.voice_client

    tracks = await player.fetch_tracks(query)

    if not tracks:
        return await inter.send("No tracks found.")

    track = tracks[0]

    await player.play(track)

    await inter.send(f"Playing {track.title}.")



# 
#   AUTH
# 


client.run(config.TOKEN)