import discord
import asyncio
import datetime
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions
import time
import sqlite3

intents = discord.Intents.all()


#startBot
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$', '/', '*'), intents=intents)



    async def on_ready(self):
        connection = sqlite3.connect('server.db')
        cursor = connection.cursor()
        await Bot.load_extension('cogs.Moderation')
        cursor.execute("""CREATE TABLE IF NOT EXISTS mutes(
            id INT,
            published id INT,
            end_time TEXT,
            reason TEXT
        )""")

        connection.commit()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


Bot = Bot()


#say
@Bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *,arg):
    deleted = await ctx.message.channel.purge(limit=1)
    await ctx.send(arg)

@Bot.command()
@commands.has_permissions(administrator=True)
async def support(ctx):
    deleted = await ctx.message.channel.purge(limit=1)
    emb= discord.Embed(title='Підтримка проєкту ❤', colour=discord.Colour.green(), description=f'Для [підтримики](https://send.monobank.ua/jar/3zLFUZLxJX) проєкту натисніть на відповідну кнопку або проскануйте QR-код нижче.')
    emb.set_image(url='https://i.imgur.com/PXzaCH2.png')
    await ctx.send(embed = emb)

#clear
@Bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=1000):
    await ctx.channel.purge (limit=amount+1)

#mute
#@Bot.command()
#@commands.has_permissions(view_audit_log=True)
#async def mute(ctx, attachment: discord.Attachment, member: discord.Member, time:int=None, *, reason='Відсутня'):
#
#    muterole = discord.utils.get(member.guild.roles, name="Muted Text")
#
#    #Перевірка
#    if muterole in member.roles:
#        await ctx.send("У цього користувача вже є мут 🙄")
#        return
#    if not member:
#        await ctx.send('Користувача не знайдено 😥')
#        return
#    if member == ctx.author:
#        await ctx.send('Ти не можеш замьютити себе 🤨')
#        return
#    if member.top_role >= ctx.author.top_role:
#        await ctx.send('Ти не можеш замьютити цього користувача! 😠')
#        return
#    if time == None:
#        await ctx.send('Ти не вказав час ⌚')
#        return
#
#    #Ембеди
#    now = datetime.datetime.now()
#    emb=discord.Embed( title = 'Гра в мовчанку', colour=discord.Colour.red(), description = f'Користувач {ctx.author.mention} замьютив користувача {member.mention} на {time} хвилин(ку).' )
#    emb.add_field(name = 'Причина:', value = f'{reason}')
#    emb.add_field(name = 'Докази:',value= f'[Тут]({attachment.url})')
#    emb.set_author(name= ctx.author.name, icon_url=ctx.author.avatar.url)
#    emb.set_footer(text = now.strftime("%d.%m • %H:%M"))
#    emb.set_image(url=attachment.url)
#
#    embls=discord.Embed( title = 'Гра в мовчанку', colour=discord.Colour.red(), description = f'Тебе було замьючено на сервері єКрафт на {time} хвилин(ну).' )
#    embls.set_author(name= ctx.author.name, icon_url=ctx.author.avatar.url)
#    embls.add_field(name = 'Видав:', value = f'{ctx.author.mention}')
#    embls.add_field(name = 'Причина:', value = f'{reason}')
#    embls.set_footer(text = now.strftime("%d.%m • %H:%M"))
#    embls.set_thumbnail(url = 'https://i.imgur.com/p6tz0tA.png')
#
#
#    channel = Bot.get_channel(1029786117689585674)
#
#
#
#    msg = await ctx.send(f'Відправлено на перевірку...')
#
#
#    class Text_mute(discord.ui.View):
#        def __init__(self):
#            super().__init__(timeout=None)
#
#        @discord.ui.button(label='Схвалити', style=discord.ButtonStyle.green)
#        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
#            await interaction.response.send_message(f'Успішно схвалено!,', ephemeral=True)
#            await interaction.message.edit(content=f'Користувач {ctx.author.mention} надіслав запит на **мут** користувача {member.mention} на **{time}** хвилин.\n\n**Причина:** {reason}.\n\n**Схвалив:** {interaction.user.mention}', view=None)
#            self.value = True
#            self.stop()
#
#        @discord.ui.button(label='Відмовити', style=discord.ButtonStyle.red)
#        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
#            await interaction.message.edit(content=f'-----------------\nКористувач {ctx.author.mention} надіслав запит на **мут** користувача {member.mention} на **{time}** хвилин.\n\n**Причина:** {reason}.\n\n**Відмовив:** {interaction.user.mention}',view=None)
#            self.value = False
#            self.stop()
#
#    view = Text_mute()
#    await channel.send(f'-----------------\n\nКористувач {ctx.author.mention} надіслав запит на **мут** користувача {member.mention} на **{time}** хвилин.\n\n**Причина:** {reason}.\n{attachment}', view=view)
#    await view.wait()
#    if view.value:
#        await member.add_roles(muterole)
#        await msg.edit(content=None, embed=emb)
#        await member.send(embed = embls)
#        print(f"Успішно виданий мут для {member.name} на {time} хвилин.\nВидав:{ctx.author.name}.\nПричина: {reason}\n-------------")
#        await asyncio.sleep (time *60)
#        await member.remove_roles(muterole)
#        print(f'Мут з користувача "{member}" знято!\n-------------')
#    else:
#        print(f'Відхилений мут для користувача {member.name}\n-------------')
#        await msg.edit(content='Відмовлено!')



#unmute
#@Bot.command()
#@commands.has_permissions(administrator=True)
#async def unmute(ctx, member:discord.Member, *, arg):
#    muterole = discord.utils.get(ctx.guild.roles, name="Muted Text")
#    vmuterole = discord.utils.get(ctx.guild.roles, name='Muted Voice')
#    if arg == 'text' or 'TEXT':
#        if muterole in member.roles:
#            await member.remove_roles(muterole)
#            await ctx.send(embed=discord.Embed(title='✅ Успішно!', description= f'Мьют текстового чату з користувача {member.mention} знято!', colour=discord.Colour.green()))
#        elif not muterole in member.roles:
#            await ctx.send(embed=discord.Embed(title='❌ Невдало!', description='У цього користувача немає мьюту текстового чату.', colour=discord.Colour.red()))
#    elif arg == 'voice' or 'VOICE':
#        if vmuterole in member.roles:
#            await member.remove_roles(vmuterole)
#            await ctx.send(embed=discord.Embed(title='✅ Успішно!', description= f'Мьют голосового чату з користувача {member.mention} знято!', colour=discord.Colour.green()))
#
#        elif not vmuterole in member.roles:
#            await ctx.send(embed=discord.Embed(title='❌ Невдало!', description='У цього користувача немає мьюту голосового чату.', colour=discord.Colour.red()))
#    else:
#        await ctx.send(embed=discord.Embed(title='❌ Невдало!', description='Перевірте правильність написання команди!.', colour=discord.Colour.red()))
#



#kick
@Bot.command()
@commands.has_permissions(view_audit_log=True)
async def kick(ctx, attachment: discord.Attachment, member: discord.Member, *, reason='Відсутня'):

    #Перевірка
    if member == ctx.author:
        await ctx.send('Ти не можеш кікнути себе себе 🤨')
        return
    if member.top_role >= ctx.author.top_role:
        await ctx.send('Ти не можеш кікнути цього користувача 🤔')
        return

    #Ембеди
    now = datetime.datetime.now()
    emb=discord.Embed( title = 'Викинуто за борт!', colour=discord.Colour.red(), description = f'Користувач {ctx.author.mention} кікнув користувача {member.mention}.' )
    emb.add_field(name = 'Причина:', value = f'{reason}')
    emb.set_author(name= ctx.author.name, icon_url=ctx.author.avatar.url)
    emb.set_footer(text = now.strftime("%d.%m • %H:%M"))

    embls=discord.Embed( title = 'Викинуто за борт', colour=discord.Colour.red(), description = f'Тебе було кікнуто з сервера єКрафт.' )
    embls.set_author(name= ctx.author.name, icon_url=ctx.author.avatar.url)
    embls.add_field(name = 'Видав:', value = f'{ctx.author.mention}')
    embls.add_field(name = 'Причина:', value = f'{reason}')
    embls.set_footer(text = now.strftime("%d.%m • %H:%M"))



    class Kick(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label='Схвалити', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(f'Успішно схвалено!,', ephemeral=True)
            await interaction.message.edit(content=f'Користувач {ctx.author.mention} надіслав запит на **кік** користувача {member.mention}.\n\n**Причина:** {reason}.\n\n**Схвалив:** {interaction.user.mention}', view=None)
            self.value = True
            self.stop()

        @discord.ui.button(label='Відмовити', style=discord.ButtonStyle.red)
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.message.edit(content=f'-----------------\nКористувач {ctx.author.mention} надіслав запит на **кік** користувача {member.mention}.\n\n**Причина:** {reason}.\n\n**Відмовив:** {interaction.user.mention}',view=None)
            self.value = False
            self.stop()

    channel = Bot.get_channel(1029786117689585674)

    view = Kick()

    msg = await ctx.send(f'Відправлено на перевірку...')
    await channel.send(f'-----------------\n\nКористувач {ctx.author.mention} надіслав запит на **кік** користувача {member.mention}.\n\n**Причина:** {reason}.\n{attachment}', view=view)
    await view.wait()
    if view.value:
        await member.send(embed=embls)
        await member.kick(reason=reason)
        await msg.edit(content=None, embed=emb)
        print(f"Успішно кікнуто користувача {member.name}.\nКікнув:{ctx.author.name}.\nПричина: {reason}\n-------------")
    else:
        print(f'Відхилений мут для користувача {member.name}\n-------------')
        await msg.edit(content='Відмовлено!')



@Bot.command()
@commands.has_permissions(administrator=True)
async def amute(ctx, member: discord.Member, time:int=None, *, reason='Відсутня'):
    muterole = discord.utils.get(member.guild.roles, name="Muted Text")

    now = datetime.datetime.now()
    emb = discord.Embed(title='Гра в мовчанку', colour=discord.Colour.red(),
                        description=f'Користувач {ctx.author.mention} замьютив користувача {member.mention} на {time} хвилин(ку).')
    emb.add_field(name='Причина:', value=f'{reason}')
    emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    emb.set_footer(text=now.strftime("%d.%m • %H:%M"))

    embls = discord.Embed(title='Гра в мовчанку', colour=discord.Colour.red(),
                          description=f'Тебе було замьючено на сервері єКрафт на {time} хвилин(ну).')
    embls.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embls.add_field(name='Видав:', value=f'{ctx.author.mention}')
    embls.add_field(name='Причина:', value=f'{reason}')
    embls.set_footer(text=now.strftime("%d.%m • %H:%M"))
    embls.set_thumbnail(url='https://i.imgur.com/p6tz0tA.png')

    await ctx.channel.purge(limit=1)
    await member.add_roles(muterole)
    await ctx.send(embed=emb)
    await member.send(embed=embls)
    print(f'Успішно виданий адмін-мут для "{member}" на {time} хвилин.\nВидав: "{ctx.author}".\nПричина: {reason}\n-------------')
    await asyncio.sleep(time * 60)
    await member.remove_roles(muterole)
    print(f'Мут з користувача "{member}" знято!\n-------------')


@Bot.command()
@commands.has_permissions(administrator=True)
async def akick(ctx, member: discord.Member, *, reason='Відсутня'):

    now = datetime.datetime.now()
    emb = discord.Embed(title='Гра в мовчанку', colour=discord.Colour.red(),
                        description=f'Користувач {ctx.author.mention} кікнув користувача {member.mention}.')
    emb.add_field(name='Причина:', value=f'{reason}')
    emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    emb.set_footer(text=now.strftime("%d.%m • %H:%M"))

    embls = discord.Embed(title='Гра в мовчанку', colour=discord.Colour.red(),
                          description=f'Тебе було кікнуто з сервера єКрафт.')
    embls.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    embls.add_field(name='Видав:', value=f'{ctx.author.mention}')
    embls.add_field(name='Причина:', value=f'{reason}')
    embls.set_footer(text=now.strftime("%d.%m • %H:%M"))
    embls.set_thumbnail(url='https://i.imgur.com/p6tz0tA.png')

    await ctx.channel.purge(limit=1)
    await ctx.send(embed=emb)
    await member.send(embed=embls)
    await member.kick(reason=reason)
    print(f'Успішно виданий адмін-кік для "{member}".\nВидав: "{ctx.author}".\nПричина: {reason}\n-------------')


#@Bot.event
#async def on_voice_state_update(member, before, after):
#    author = member.id
#    if before.channel is None and after.channel is not None:
#        print('1')
#        t1 = time.time()
#        tdict[author] = t1
#    elif before.channel is not None and after.channel is None and author in tdict:
#        t2 = time.time()
#        print('0')
#        print(t2-tdict[author])


#ERRORS
#@mute.error
#async def mute_error(ctx, error):
#    if isinstance(error, commands.MissingPermissions):
#        await ctx.send(embed=discord.Embed(title= '✋ Ти не можеш використовувати цю команду!', colour=discord.Colour.red()))
#    if isinstance(error, commands.MissingRequiredAttachment):
#        await ctx.send(embed=discord.Embed(title= '✋ Ти не прикріпив докази!', colour=discord.Colour.red()))
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send(embed= discord.Embed(title='Перевір правильність написання команди!',colour=discord.Colour.red()))
#
#@kick.error
#async def kick_error(ctx, error):
#    if isinstance(error, commands.MissingPermissions):
#        await ctx.send(embed=discord.Embed(title='✋ Ти не можеш використовувати цю команду!', colour=discord.Colour.red()))
#    if isinstance(error, commands.MissingRequiredAttachment):
#        await ctx.send(embed=discord.Embed(title='✋ Ти не прикріпив докази!', colour=discord.Colour.red()))
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send(embed=discord.Embed(title='Перевір правильність написання команди!', colour=discord.Colour.red()))
#    if isinstance(error, commands.MemberNotFound):
#        await ctx.send(embed=discord.Embed(title='Користувача не знайдено 😥', colour=discord.Colour.red()))
#
#@akick.error
#async def akick_error(ctx, error):
#    if isinstance(error, commands.MissingPermissions):
#        await ctx.send(embed=discord.Embed(title='✋ Ти не можеш використовувати цю команду!', colour=discord.Colour.red()))
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send(embed=discord.Embed(title='Перевір правильність написання команди!', colour=discord.Colour.red()))




Bot.run('TOKEN')
