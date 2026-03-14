import discord
from discord import app_commands
import random
from discord.ext import commands
from collections import deque, defaultdict
import re
import json
import os

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

mask={"a" : "initialize"}
cookie={"a" : "initialize"}
# ---------- Events ----------

@bot.event
async def on_ready():
    if os.path.exists("botData.json"):
        global mask
        with open("botData.json", "r") as f:
            mask = json.load(f)
    if os.path.exists("botData2.json"):
        global cookie
        with open("botData2.json", "r") as f:
            cookie = json.load(f)
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()




# ---------- Slash Commands ----------

@bot.tree.command(name="whisper", description="Say something anonymously")
@app_commands.describe(text="what can you say?")
async def whisper(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(
        "Sent.",
        ephemeral=True
    )
    if cookie[str(interaction.user.id)] in mask:
        faName = mask[cookie[str(interaction.user.id)]]
    else:
        faName = f"Anon"
    await interaction.channel.send(f" {faName}<{cookie[str(interaction.user.id)]}>: {text}")

@bot.tree.command(name="set", description="set a new name for your current cookie")
@app_commands.describe(text="new name")
async def set(interaction: discord.Interaction, text: str):
    global mask
    mask[cookie[str(interaction.user.id)]]=text
    with open("botData.json", "w") as f:
        json.dump(mask, f, indent=4)
    await interaction.response.send_message(
        "Done.",
        ephemeral=True
    )
    
@bot.tree.command(name="generate", description="generate a new cookie")
@app_commands.describe()
async def generate(interaction: discord.Interaction):
    del mask[cookie[str(interaction.user.id)]]
    i=random.randrange(1, 10000)
    while str(i) in cookie.values():
        i=random.randrange(1, 10000)
    cookie[str(interaction.user.id)]=str(i)
    with open("botData2.json", "w") as f:
        json.dump(cookie, f, indent=4)
    await interaction.response.send_message(
        "Done.",
        ephemeral=True
    )

@bot.tree.command(name="show", description="Upload an image")
@app_commands.describe(image="The image you want to upload")
async def show(interaction: discord.Interaction, image: discord.Attachment):
    # Check if the file is actually an image
    if image.content_type.startswith("image/"):
        await interaction.response.send_message(
            "Sent.",
        ephemeral=True
        )
        if str(interaction.user.id) in mask:
            faName = mask[cookie[str(interaction.user.id)]]
        else:
            faName = f"Anon"
        await interaction.channel.send(f"{faName}<{cookie[str(interaction.user.id)]}>: {image.url}")
    else:
        await interaction.response.send_message("That's not an image file!", ephemeral=True)                   


# ---------- Run ----------

bot.run(#insert discord bot token here)
