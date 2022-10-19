import os
import discord
import discord.utils
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")

default_intents = discord.Intents.default()
default_intents.message_content = True
default_intents.members = True
default_intents.presences = True

bot = commands.Bot(command_prefix='dakkytest ', intents=default_intents, help_command=None)


# CLASSIC ON READY
@bot.event
async def on_ready():
    print(f"{bot.user.display_name} est connecté au serveur !")


# ON JOINING MEMBER
@bot.event
async def on_member_join(user: discord.Member):
    general_channel: discord.TextChannel = bot.get_channel(1014600921839321140)
    await general_channel.send(content=f"Bienvenue {user.mention}, amuse toi bien ici !")


# KICK COMMAND
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
    try:
        await user.kick(reason=reason)
        embed = discord.Embed(color=discord.Colour.red(), title="", description="")
        embed.add_field(name="Kick:", value=f"""
**{user}** a été kick par {ctx.author.display_name}.
Raison = **{reason}**
""", inline=True)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(color=discord.Colour.red(), title="", description="")
        embed.add_field(name="Error:", value=f"""
Error
""", inline=True)
        await ctx.send(embed=embed)


# BAN COMMAND
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    try:
        await user.ban(reason=reason)
        embed = discord.Embed(color=discord.Colour.red(), title="", description="")
        embed.add_field(name="Ban:", value=f"""
**{user}** a été ban par {ctx.author.display_name}.
Raison = **{reason}**
""", inline=True)
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(color=discord.Colour.red(), title="", description="")
        embed.add_field(name="Error:", value=f"""
Error
""", inline=True)
        await ctx.send(embed=embed)


# UNBAN COMMAND BUT DOESN'T WORK NOW
@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member: discord.User):
    try:
        banned_users = await discord.Guild.fetch_ban(user)
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await unban(discord.User)
                embed = discord.Embed(color=discord.Colour.blue(), title="", description="")
                embed.add_field(name="Unban:", value=f"""
**{user}** a été unban par {ctx.author.display_name}.
""", inline=True)
                await ctx.send(embed=embed)
                return
    except discord.NotFound:
        embed = discord.Embed(color=discord.Colour.blue(), title="", description="")
        embed.add_field(name="Error:", value=f"""
Utilisateur introuvable.
""", inline=True)
        await ctx.send(embed=embed)


# CLEAR COMMAND
@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.channel.send(f"{amount} messages on été supprimé.")


# SAY HI TO THE BOT 
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello !")


# FOR TEST IF THE BOT IS UP
@bot.command()
async def ping(ctx):
    await ctx.send('pong')


# MY GITHUB LINK
@bot.command()
async def github(ctx):
    embed = discord.Embed(color=discord.Colour.blue(), title="Github", description="Le github de mon créateur !")
    embed.set_author(name="Clique ici !", url="https://github.com/Aptura",
                     icon_url="https://avatars.githubusercontent.com/u/31808221?v=4")
    await ctx.send(embed=embed)


# HELPING COMMAND
@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed(
        title="Help",
        description="Toute l'aide dont tu a besoin",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Information demandé par: {}".format(ctx.author.display_name))
    embed.add_field(name="Admin", value="`clear <nombre>`, `kick <@name> <raison>`, `ban <@name> <raison>`")
    embed.add_field(name="Divers", value="`hello`, `ping`, `github`", inline=False)
    embed.add_field(name="Help", value="`help`", inline=False)
    await ctx.send(embed=embed)


# ERROR CASE
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument.")
    elif isinstance(error, commands.CommandError):
        await ctx.send("La commande n'a pas abouti ou n'existe pas.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas la permission de faire cela !")


# RUN THE BOT
bot.run(os.getenv("TOKENTEST"))
