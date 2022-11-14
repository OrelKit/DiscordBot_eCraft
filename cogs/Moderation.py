import discord
from discord.ext import commands, tasks
import datetime
import sqlite3
import asyncio

connection= sqlite3.connect('server.db')
cursor= connection.cursor()


class Moderation(commands.Cog):

    def __init__(self, Bot):
        self.Bot = Bot

    @tasks.loop()
    async def check_mutes(self):
        current = datetime.datetime.now()
        time = cursor.execute("SELECT end_time FROM mutes")
        unmute = datetime.datetime.strptime(str(time), "%c")
        if unmute < current:
            user_id = cursor.execute("SELECT id FROM mutes")
            try:
                member = await self.guild.fetch_member(int(user_id))
                await member.remove_roles(self.mutedrole)
                cursor.execute(f'DELETE FROM mutes WHERE id = {member.id}')
                connection.commit()
                print('Ready!')
            except discord.NotFound:
                pass


    @commands.command()
    async def mute(self, ctx, member: discord.Member, time: int=None, *, reason=None):
        end_time=datetime.datetime.now() + datetime.timedelta(minutes=time)
        cursor.execute(f"INSERT INTO mutes VALUES ({member.id},{ctx.author.id},'{end_time}', '{reason}')")
        connection.commit()
        await asyncio.sleep (time *60)
        cursor.execute(f'DELETE FROM mutes WHERE id = {member.id}')
        connection.commit()
        await ctx.message.add_reaction('✅')






async def setup(bot):
    await bot.add_cog(Moderation(bot))