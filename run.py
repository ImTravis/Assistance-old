import discord
from discord.ext import commands

import sys
import asyncio
import os

from os import remove
from sys import argv

# Options.
NAME = 'Assistance' # Name of the bot, this is used on many messages.
VERSION = '1.0' # Current version of the bot.
AUTHOR = 'Travis#9729' # The author of the bot, if you change this you won't be able to launch this bot. This is my anti-skid mech..
SUPPORTROLE_NAME = 'Support' # The name of the support role on your server.
GLOBAL_IMAGE = 'https://travis.cool/images/ticket.png' # This image is used on all embed messages, exluding a few. You can change this to whatever you want.
FOOTER = 'Testing.' # This is the footer of all embed messages, you can change this to whatever you want.
TICKETS = 'tickets.txt' # This is the file where all open tickets' channels are stored. This helps the 'close' command to check if a ticket is open.
USERS = 'users.txt' # This file tracks who has a ticket open and who doesn't.
CLOSING_TIME = 30 # This is the time it takes before a ticket is closed after the 'close' command is called. You can change this to anything, but it has to be a number.
COMMANDS_CHANNEL = '543100912294559749' # This is the channel ID where the bot's commands are allowed.
# Personalization options.
SUPPORT_ONLY_CLOSE = 'true' # Should support team members be the only people who can close a ticket?

TOKEN = 'token' # Your bot token, paste this here. -- DO NOT SHARE THIS WITH ANYONE! --
PREFIX = '!' # Prefix that is used for all commands, change this to whatever you like the most.

client = commands.Bot(command_prefix=PREFIX)
client.remove_command('help')

@client.event
async def on_ready():
    print('Running...')
    await client.change_presence(game=discord.Game(type=2, name='your commands.'))

@client.command(pass_context=True)
async def new(ctx):
	member = ctx.message.author.name
	memberfull = ctx.message.author
	memberid = ctx.message.author.id
	channel = ctx.message.channel.id
	server = ctx.message.author.server
	supportrole = discord.utils.get(memberfull.server.roles, name=SUPPORTROLE_NAME)
	with open(USERS, 'r') as file:
		lines = file.readlines()
	lines = [line.strip() for line in lines]
	if channel == COMMANDS_CHANNEL:
		if memberid in lines:
			await client.say("**Error:** You already have a ticket open. *Hint: The ticket has your Discord name in it.*")
		if memberid not in lines:
			everyone = discord.PermissionOverwrite(read_messages=False)
			mine = discord.PermissionOverwrite(read_messages=True)
			createchannel = await client.create_channel(server, ''+member+'-ticket', (server.default_role, everyone), (memberfull, mine), (supportrole, mine))
			ccid = createchannel.id
			# Print user to USERS file.
			with open(USERS, "a") as file:
				file.write("{}\n".format(memberid))
			# Print new channel ID to TICKETS file.
			with open(TICKETS, "a") as file:
				file.write("{}\n".format(ccid))
			await client.say("Your support ticket has opened here: <#"+ccid+">")
			embed=discord.Embed(title=""+NAME+" | Ticket Opened.")
			embed.set_thumbnail(url=GLOBAL_IMAGE)
			embed.add_field(name="Information:", value="Thank you for making a ticket, how can we assist you today?", inline=False)
			embed.add_field(name="Opened By:", value="<@"+memberid+">", inline=False)
			embed.set_footer(text=FOOTER)
			tag = await client.send_message(client.get_channel(str(ccid)), '<@'+memberid+'> {}'.format(supportrole.mention))
			await client.delete_message(tag)
			await client.send_message(client.get_channel(str(ccid)), embed=embed)
			await client.edit_channel(client.get_channel(str(ccid)), topic="Ticket opened by: <@"+memberid+">")
			await client.move_channel(client.get_channel(str(ccid)), 0)
	else:
		pass

@client.command(pass_context=True)
async def close(ctx):
	channel = ctx.message.channel.id
	userid = ctx.message.author.id
	user = ctx.message.author
	with open(TICKETS, 'r') as file:
		lines = file.readlines()
	lines = [line.strip() for line in lines]
	if channel in lines:
		embed=discord.Embed(title=""+NAME+" | Ticket Closing.")
		embed.set_thumbnail(url=GLOBAL_IMAGE)
		embed.add_field(name="Information:", value="Thank you for making a ticket, it is now closing in `"+str(CLOSING_TIME)+" seconds`. Hopefully your issue/question was resolved, have a great day!", inline=False)
		embed.add_field(name="Closed By:", value="<@"+userid+">", inline=False)
		embed.set_footer(text=FOOTER)
		await client.send_message(client.get_channel(str(channel)), embed=embed)
		await asyncio.sleep(CLOSING_TIME)
		await client.delete_channel(client.get_channel(str(channel)))
		# Delete ticket channel ID from TICKETS file.
		with open(r''+TICKETS+'', 'r') as file:
			filedata = file.read()
			filedata = filedata.replace('{}'.format(channel), '')
		with open(r''+TICKETS+'', 'w') as file:
			file.write(filedata)
			file.close()
		# Delete user's ID from USERS file.
		with open(r''+USERS+'', 'r') as file:
			filedata = file.read()
			filedata = filedata.replace('{}'.format(userid), '')
		with open(r''+USERS+'', 'w') as file:
			file.write(filedata)
			file.close()
		await client.send_message(user, '')
	if channel not in lines:
		pass

# Do not change anything below this line unless you know what you are doing.
dev_version = '1.0'

client.run(TOKEN)
