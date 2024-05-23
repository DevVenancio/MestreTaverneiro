import discord
import os
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from dotenv import load_dotenv
from announcement import AnunciosModal

intents = discord.Intents.all()
intents.message_content = True
bot: Bot = commands.Bot(command_prefix='t!', intents=intents)
load_dotenv()

# --- EVENTOS --- #

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Online como {bot.user}')


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


# --- COMANDOS --- #

@bot.tree.command(description='Comando para o Anúncio de Mesas')
async def anunciar_mesa(interact: discord.Interaction):
    await interact.response.send_modal(AnunciosModal())
    

@bot.command(name='oi')
async def say_hello(ctx: commands.Context):
    author_name = ctx.author.name
    response = f"Olá, {author_name}."
    await ctx.send(response)

bot.run(os.getenv("BOT_TOKEN"))
