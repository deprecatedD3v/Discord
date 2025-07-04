import discord
from discord.ext import commands
from config import Config

class Events(commands.Cog):
    """Event listeners for the bot."""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = next((c for c in member.guild.text_channels if c.permissions_for(member.guild.me).send_messages), None)
        if channel:
            embed = discord.Embed(
                title="👋 Welcome!",
                description=f"Welcome to the server, {member.mention}!",
                color=Config.EMBED_COLORS['success']
            )
            await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = next((c for c in member.guild.text_channels if c.permissions_for(member.guild.me).send_messages), None)
        if channel:
            embed = discord.Embed(
                title="😢 Goodbye!",
                description=f"{member.display_name} has left the server.",
                color=Config.EMBED_COLORS['error']
            )
            await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permission Error",
                description="You don't have permission to use this command!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏰ Cooldown",
                description=f"Please wait {error.retry_after:.2f} seconds before using this command again.",
                color=Config.EMBED_COLORS['warning']
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title="❌ Error",
            description="An unexpected error occurred. Please try again later.",
            color=Config.EMBED_COLORS['error']
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Events(bot)) 