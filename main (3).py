import os
import discord
from discord import Member
from discord.utils import get
import random
import asyncio
import time
from discord.ext import commands, tasks
from random import choice
from webserver import keep_alive
import random
from random import randint
import sys
import replit
from replit import db

token = os.environ['token']
client = commands.Bot(command_prefix="$", intents=discord.Intents.all())
client.remove_command("help")
@client.event


async def on_ready():
	print("Bot is online and ready to serve!")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f" $help"))




@client.command()
async def warn(ctx, member: discord.Member, *, reason=None):
	if isinstance(ctx.channel, discord.channel.DMChannel):
		em = discord.Embed(title="❌ | DM Commands", description="You can't use this commands in the bot's DMs, please go back to the server and try there", colour=discord.Colour.red())
		alert=await ctx.reply(embed=em, mention_author=False)
	else:
		em = discord.Embed(title="🔔 | Warn User", description="Warning User...Please Wait", colour=discord.Colour.green())
		alert=await ctx.reply(embed=em, mention_author=False)
		try:
			if reason == None:
				em = discord.Embed(title="❌ | Warn Error", description="You must enter a reason to warn the user", colour=discord.Colour.red())
				await alert.edit(embed=em, mention_author=False)
			else:
				em = discord.Embed(title="Warning", description=f"You have been sent a warning from {ctx.author}. Reason: ```{reason}```", colour=discord.Colour.green())
				await member.send(embed=em)
				rand_value = random.randint(1,100000000)
				try:
					db[f'warn{member.id}/{rand_value}']=reason
					em = discord.Embed(title="🔔 | Warn User", description=f"The case has been recorded under `warn{member.id}/{rand_value}`. To get all cases for this person, type `$cases <member>`", colour=discord.Colour.green())
					await alert.edit(embed=em, mention_author=False)
				
				except:
					em = discord.Embed(title="❌ | Warn Error", description="Database Error, Please try again", colour=discord.Colour.red())
					await alert.edit(embed=em, mention_author=False)
		except:
			em = discord.Embed(title="❌ | Warn Error", description="Something went wrong, please try again", colour=discord.Colour.red())
			await alert.edit(embed=em, mention_author=False)
		
								

@client.command()
async def cases(ctx, member:discord.Member):
	list = []
	em = discord.Embed(title="🔎 | Finding Cases", description=f"Please wait...Finding All Cases for {member.mention}", colour=discord.Colour.green())
	alert=await ctx.reply(embed=em, mention_author=False)
	try:
		key = f'warn{member.id}'
		print(member.id)
		matches = db.prefix(key)
		list = []
		for matches in db.keys():
			list.append(matches)
		em = discord.Embed(title=f"🔎 | Cases for {member}", description=f"\n".join(list), colour=discord.Colour.green())
		await alert.edit(embed=em, mention_author=False)
	except:
		em = discord.Embed(title="❌ | Error", description=f"Something went wrong, please try again", colour=discord.Colour.red())
		await alert.edit(embed=em, mention_author=False)



@client.command()
async def remove_cases(ctx, member:discord.Member):
	em = discord.Embed(title="🗑️ | Delete All Cases", description=f"Please wait...Deleting All Cases for {member.mention}", colour=discord.Colour.green())
	alert=await ctx.reply(embed=em, mention_author=False)
	try:
		key = f'warn{member.id}'
		matches = db.prefix(key)
		for matches in db.keys():
			del db[matches]
			em = discord.Embed(title="🗑️ | Deleting All Cases", description=f"Deleted {matches}", colour=discord.Colour.green())
			await alert.edit(embed=em, mention_author=False)
			await ctx.send(f'deleted {matches}')
		await ctx.send('Deleted All for this user')
		em = discord.Embed(title="🗑️ | Deleted All Cases", description=f"Successfully deleted all cases for {member.mention}", colour=discord.Colour.green())
		await alert.edit(embed=em, mention_author=False)
	except:
		em = discord.Embed(title="❌ | Error", description=f"Something went wrong, please try again", colour=discord.Colour.red())
		await alert.edit(embed=em, mention_author=False)
keep_alive()
client.run(token)


