import discord
from discord.ext import commands
from datetime import timedelta
import pytz

permision_embed = discord.Embed(title="Erreur - Permissions", description=f"Vous n'avez pas la permissin d'utiliser cette commande", color=0xFF0000)
client = commands.Bot(command_prefix = "!", intents=discord.Intents.all(), help_command=None)
token = input("token: ")

@client.event
async def on_ready():
    print(f'Connecté en tant que { client.user}')

@client.event
async def on_member_join(member):
    print(member)
    embed=discord.Embed(title="Nouveau membre !" , description=f"Bienvenue sur le serveur {member.mention}")
    embed.set_thumbnail(url=member.avatar)
    await member.guild.system_channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    print(f"Le membre {member} vient de quitter le serveur.")
    await member.guild.system_channel.send(f"{member.mention} nous quitte...")


@client.command()
async def serverinfo(ctx):
    guild = ctx.message.guild
    embed=discord.Embed(title=guild.name)
    embed.add_field(name="Propriétaire", value=guild.owner, inline=True)
    embed.add_field(name="Membres", value=len(guild.members), inline=True)
    embed.add_field(name="Boosts", value=ctx.guild.premium_subscription_count, inline=True)
    embed.add_field(name=f"Rôles - {len(ctx.guild.roles) - 1}", value=", ".join([str(r.mention) for r in ctx.guild.roles if r.name != '@everyone']), inline=False)
    embed.set_footer(icon_url=ctx.message.author.avatar, text=f"Demandé par {ctx.message.author}")
    await ctx.send(embed=embed)

@client.command()
async def kick(ctx, member: discord.User, reason = "Non spécifiée"):
    if ctx.message.author.guild_permissions.kick_members:
        guild = ctx.message.guild
        member = guild.get_member(int(member.id))
        await member.kick(reason=reason)
        embed=discord.Embed(title="Kick", description=f"Le membre **{member}** à été explusé par <@{ctx.message.author.id}> \n > Raison : {reason}", color=0x0000FF)
        await ctx.send(embed=embed)
    else:
        await ctx.reply(embed=permision_embed)
@client.command()
async def ban(ctx, member : discord.User, reason = None):
    if ctx.message.author.guild_permissions.ban_members:
        guild = ctx.message.guild
        member = guild.get_member(int(member.id))
        await member.ban(reason=reason)
        embed=discord.Embed(title="Bannissement", description=f"Le membre **{member}** à été banni par <@{ctx.message.author.id}> \n > Raison : {reason}", color=0x0000FF)
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=permision_embed)

@client.command()
async def mute(ctx, member: discord.Member, until: int, *, reason = "Non spécifiée"):
    if ctx.message.author.guild_permissions.moderate_members:
        await member.timeout(timedelta(minutes=until), reason=reason)
        await ctx.send(embed=discord.Embed(title="Mute", description=f"Le membre **{member}** à été exclu par <@{ctx.message.author.id}> \n > Raison : {reason} \n >  Temps : {until} minutes", color=0x0000FF))
    elif member == ctx.message.author:
        await ctx.send(embed=discord.Embed(title="Erreur", description="Vous ne pouvez pas vous exclure vous même !", color=0xFF0000))
    else:
        await ctx.send(embed=permision_embed)


@client.command()
async def unban(ctx, member):
    if ctx.message.author.guild_permissions.ban_members:
        print(ctx.message.author)
        guild = ctx.message.guild
        async for ban in guild.bans():
            if (f'{ban.user.name}#{ban.user.discriminator}') == member:
                embed=discord.Embed(title="Débanissement", description=f"{ctx.message.author} a revoqué le bannisement de {ban.user.name}#{ban.user.discriminator}")
                await ctx.send(embed=embed)
                await guild.unban(ban.user)
            else:
                embed=discord.Embed(description=f"Impossible de trouver {member} dans la liste des bannissements", color=0xFF0000)
                await ctx.send(embed=embed)
    else:
        await ctx.send(embed=permision_embed)
    
@client.command()
async def clear(ctx, limit = 10000):
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=int(limit))
    else:
        await ctx.send(embed=permision_embed)

@client.command()
async def help(ctx, command = None):
    embed = discord.Embed(
        title="Liste des commandes :",
        description='''
        !help : affiche l'aide sur la commande
        !kick `membre*` `raison`: expulser un membre
        !ban `membre*`, `raison`: bannir un membre
        !clear : supprimer les messages d'un salon
        !mute `membre*` `temps (minutes)*` `raison`: exclure un membre
        !unban `membre*`: debannir un membre
        !serverinfo : afficher les informations sur le serveur
        !userinfo `utilisateur*(laisser vide si soi-même)` : afficher les informations sur l'utilisateuer

        * = obligatoire
        '''
        )
    await ctx.send(embed = embed)

@client.command()
async def gay(ctx, member : discord.Member):
    if ctx.message.author.id == 1064496413897142323:
        await ctx.send("Non, Nikta, tu es blacklist")
    else:
        #role = ctx.message.guild.get_role(1091738060493959259)
        role = ctx.message.guild.get_role(1091764979121782794)
        if not member.id == 877198695186169877:
            await member.add_roles(role)

@client.command()
async def say(ctx, messagelink):
    await ctx.message.delete()
    channelid = messagelink[49:68]
    channel = ctx.message.guild.get_channel(int(channelid))
    messages = channel.history(limit=200)
    async for message in channel.history(limit=(200)):
        if message.id == int(messagelink[69:88]):
            webhook = await message.channel.create_webhook(name=message.author, avatar=await message.author.avatar.read())
            await webhook.send(message.content)


@client.command()
async def wbclear(ctx):
    guild = ctx.message.guild
    webhooks = await guild.webhooks()
    for webhook in webhooks:
        await webhook.delete()

    

@client.command()
async def userinfo(ctx, user : discord.Member = None):
    guild = ctx.message.guild
    if user == None:
        user = ctx.message.author
    embed=discord.Embed()
    embed.add_field(name="Tag", value=f'#{user.discriminator}', inline=True)
    embed.add_field(name="Identifiant", value=user.id, inline=True)
    embed.add_field(name=f"Rôles - {len(user.roles) - 1}", value=", ".join([r.mention for r in user.roles if r.name != '@everyone']), inline=False)
    embed.add_field(name="Création du compte", value=discord.utils.format_dt(user.created_at))
    embed.add_field(name="Arivée sur le serveur", value=discord.utils.format_dt(user.joined_at))
    embed.set_author(name=f"Informations à propos de {user.name}", icon_url=user.avatar)
    embed.set_footer(icon_url=ctx.message.author.avatar, text=f"Demandé par {ctx.message.author}")
    await ctx.send(embed=embed)
client.run(token)
