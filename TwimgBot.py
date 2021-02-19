# twimgbot.py
import os
import tweepy
import discord
import json
import random
import re
from dotenv import load_dotenv

# api tokens
load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')
GUILD=os.getenv('DISCORD_GUILD')
client=discord.Client()

auth=tweepy.OAuthHandler(
	os.getenv('CONSUMER_KEY'),
	os.getenv('CONSUMER_SECRET'))
auth.set_access_token(
	os.getenv('ACCESS_TOKEN'),
	os.getenv('ACCESS_SECRET'))
twapi=tweepy.API(auth,wait_on_rate_limit=True)

@client.event
async def on_ready():
	guild = discord.utils.get(client.guilds)

	print(
		f'{client.user} is connected to server:\n'
		f'{guild.name}(id: {guild.id})'
	)

@client.event
async def on_message(message):
	# ignores its own messages
	if message.author == client.user:
		return

	# grabs a random tweet with image from given twitter user
	if re.match(r'!img*',message.content):
		try:
			tweets = []
			account = (message.content[4:]).strip()

			# grabs tweets through twitter api. collects those with media
			for status in twapi.user_timeline(screen_name=account,count=200):
				if 'media' in status.entities:
					tweets.append(status)
			
			chosen = random.choice(tweets)

			id = json.dumps(chosen.id, indent=4, sort_keys=True)
			screenname = json.dumps(chosen.user.screen_name, indent=4, sort_keys=True)
			screenname = screenname.replace("\"","")
			print(f'https://twitter.com/{screenname}/status/{id}')
			await message.channel.send(f'https://twitter.com/{screenname}/status/{id}')

		except:
			print(f'Error occurred. Probably invalid twitter username.')
			await message.channel.send(f'Error occurred. Probably invalid twitter username.')

client.run(TOKEN)