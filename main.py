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


@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(1213694993324310599)
    welcome_image = discord.File("src/img/welcome.gif", "welcome.gif")

    welcome_embed = discord.Embed(title=f"Bem-Vindo {member.name}!", description="Sinta-se à vontade :)")
    welcome_embed.set_image(url="attachment://welcome.gif")
    welcome_embed.set_thumbnail(url=member.avatar)
    welcome_embed.color = discord.Color.green()

    await channel.send(files=[welcome_image], embed=welcome_embed)


@bot.event
async def on_member_remove(member: discord.Member):
    channel = bot.get_channel(1213695022923517952)
    bye_image = discord.File("src/img/bye.gif", "bye.gif")

    bye_embed = discord.Embed(title="Vá em paz...", description="Infelizmente não gostou do ambiente :(")
    bye_embed.set_image(url="attachment://bye.gif")
    bye_embed.set_thumbnail(url=member.avatar)
    bye_embed.color = discord.Color.red()

    await channel.send(files=[bye_image], embed=bye_embed)

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
