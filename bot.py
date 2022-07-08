import discord
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from utils.tgd import get_new_articles
import json


# Logger related
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def send_tgd_msg(tgd_article, guild, channel_id, msg_format):
    article_link = 'https://tgd.kr/s/{0}'.format(tgd_article['article_id'])
    channel = guild.get_channel(int(channel_id))
    print(channel)
    print(msg_format.format(link=article_link))
    channel.send(msg_format.format(link=article_link))
    

# Scheduler related
scheduler = BackgroundScheduler()
@scheduler.scheduled_job('interval', seconds=5, id='update_tgd')
def check_tgd_updates():
    with open('data/data.json') as data_file:
        data = json.load(data_file)
    for guild in client.guilds:
        guild_id = str(guild.id)
        if guild_id in data:
            for tgd_data in data[guild_id]['tgd']:
                new_articles = get_new_articles(tgd_data['streamer_id'], last_update=tgd_data['last_update'])
                for new_article in new_articles:
                    send_tgd_msg(new_article, guild, tgd_data['channel_id'], tgd_data['msg_format'])
                if new_articles:
                    tgd_data['last_update']=new_articles[-1]['article_id']
            with open('data/data.json', 'w', encoding='utf8') as data_file:
                data = json.dump(data, data_file, ensure_ascii=False)


# Discord Bot related
client = discord.Client()

@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))
    scheduler.start()
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('@everyone Hello!')

if __name__ == '__main__':
    with open('data/token.json') as token_file:
        discord_token = json.load(token_file)['discord']
    client.run(discord_token)
