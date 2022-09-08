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
