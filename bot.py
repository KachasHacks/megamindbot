import os
import random
import requests
import json

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", "")
DISCORD_GUILD = os.getenv("DISCORD_GUILD", "Test")
API_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

API_URL = "https://api-inference.huggingface.co/models/"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="?")


def query(payload):
    model = "gpt2"
    data = json.dumps(payload)
    response = requests.request("POST", f"{API_URL}{model}", headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord")


@bot.command(name="ama", help="Ask me anything...I double dare you")
async def ama(ctx, *, question):
    resp = query({"inputs": question})
    answer = resp[0]["generated_text"]
    print(answer)
    await ctx.send(answer)


@bot.command(name="trivia", help="Give me a trivia question")
async def trivia(ctx):
    response = requests.request(
        "GET", "https://opentdb.com/api.php?amount=50&category=18"
    )
    questions = response.json()
    question = random.choice(questions["results"])
    await ctx.send(question["question"])


bot.run(TOKEN)

# client = discord.Client(intents=intents)


# @client.event
# async def on_ready():
# guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
# print(f"{client.user} has connected to Discord:\n {guild.name} (id: {guild.id})")

# members = "\n - ".join([member.name for member in guild.members])
# print(f"Guild Members:\n - {members}")


# @client.event
# async def on_member_join(member):
# await member.create_dm()
# await member.dm_channel.send(
# f"Hello {member.name}, welcome to your last Discord server!"
# )


# @client.event
# async def on_message(message):
# if message.author == client.user:
# return

# if message.content == "99!":
# response = random.choice(
# ["Hello", "wooza", "scrubs rewatch show with zac and donald"]
# )
# await message.channel.send(response)
# elif message.content == "raise-exception":
# raise discord.DiscordException


# @client.event
# async def on_error(event, *args, **kwargs):
# with open("err.log", "a") as f:
# if event == "on_message":
# f.write(f"Unhandled message: {args[0]}\n")
# else:
# raise


# client.run(TOKEN)
