import nextcord
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands

import time

import openai

openai.api_key = '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'


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


@client.slash_command(dm_permission=False, name='ukraine', description='Glory to Ukraine', description_localizations={'uk': 'Показова кара #ХлопчикУТрусиках', 'ru': 'fuck russia'})
async def ukraine(inter: nextcord.Interaction):

    query = 'Гимн Украины — "Ще не вмерла України і слава, і воля"'

    if not inter.guild.voice_client:
        player = await inter.user.voice.channel.connect(cls=mafic.Player)
    else:
        player = inter.guild.voice_client

    print(inter.guild.voice_client)
    print(inter.user.voice.channel)


    tracks = await player.fetch_tracks(query)

    track = tracks[0]

    await player.play(track)

    await inter.send('https://usagif.com/wp-content/uploads/2022/4hv9xm/ukrainian-waving-flag-1.gif')



# 
# 
#   MUSIC
# 
# 


@client.slash_command(name='join', description='Join voice channel', description_localizations={'uk': 'Підключити до голосового каналу', 'ru': 'Подключить к голосовому каналу'})
async def join_cmd(inter: Interaction, channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice], description='Select voice channel', required=True, description_localizations={'uk': 'Вибери голосовий канал', 'ru': 'Выбери голосовой канал'})):
    if not inter.guild.voice_client:
        await channel.connect()
        await inter.send(f'Connected to {channel}')
    else:
        await inter.guild.voice_client.disconnect()
        await channel.connect()
        await inter.send(f'Connected to {channel}')





@client.slash_command(dm_permission=False, name='play', description='Play music', description_localizations={'uk': 'Відтворення музики з YouTube', 'ru': 'Воспроизведение музыки из YouTube'})
async def play(inter: nextcord.Interaction, query: str = SlashOption(name='search', description='Music to play', required=True, description_localizations={'uk': 'Назва музики', 'ru': 'Название музыки'})):
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


@client.slash_command(name='leave', description='Leave voice channel', description_localizations={'uk': 'Вимкнути бота від голосового чату', 'ru': 'Отключить бота от голосового чата'})
async def leave_cmd(inter: Interaction):
    vc = inter.guild.voice_client

    await vc.disconnect()
    await inter.send('Disconnected')




@client.slash_command(name='ask', description='Ask ChatGPT')
async def ask_cmd(inter: nextcord.Interaction, msgprompt: str = SlashOption(name='prompt', description='Ask GPT', required=True)):

    await inter.send(f'You asked me about {msgprompt}')

    response = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = msgprompt,
        max_tokens = 200,
        temperature = 0.5,
        top_p = 1.0,
        frequency_penalty = 0.5,
        presence_penalty = 0.0,
    )
    
    await inter.send(response['choices'][0]['text'])



client.run(config.TOKEN)