import discord
from discord.ext import commands
from config import Config
import platform
import psutil
import time

class General(commands.Cog):
    """General utility commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
    
    @commands.command(name="ping")
    @commands.cooldown(1, Config.COOLDOWNS['default'], commands.BucketType.user)
    async def ping(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**",
            color=Config.EMBED_COLORS['info']
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="help")
    @commands.cooldown(1, Config.COOLDOWNS['default'], commands.BucketType.user)
    async def help_command(self, ctx):
        """Show help information about available commands."""
        embed = discord.Embed(
            title="🤖 Bot Help",
            description="Here are the available commands:",
            color=Config.EMBED_COLORS['info']
        )
        
        # General commands
        general_commands = [
            "`!ping` - Check bot latency",
            "`!help` - Show this help message",
            "`!info` - Show bot information",
            "`!userinfo [user]` - Show user information"
        ]
        
        # Admin commands
        admin_commands = [
            "`!kick <user> [reason]` - Kick a user",
            "`!ban <user> [reason]` - Ban a user",
            "`!clear <amount>` - Clear messages",
            "`!mute <user> <duration>` - Mute a user",
            "`!createroles` - Create all role categories",
            "`!deleteroles` - Delete all bot-created roles"
        ]
        
        # Fun commands
        fun_commands = [
            "`!8ball <question>` - Ask the magic 8-ball",
            "`!roll [dice]` - Roll dice",
            "`!coinflip` - Flip a coin",
            "`!joke` - Get a random joke"
        ]
        
        # Role commands
        role_commands = [
            "`!roles` - Show role categories and manage roles"
        ]
        
        embed.add_field(
            name="📋 General Commands",
            value="\n".join(general_commands),
            inline=False
        )
        embed.add_field(
            name="⚙️ Admin Commands",
            value="\n".join(admin_commands),
            inline=False
        )
        embed.add_field(
            name="🎮 Fun Commands",
            value="\n".join(fun_commands),
            inline=False
        )
        
        embed.add_field(
            name="🎭 Role Commands",
            value="\n".join(role_commands),
            inline=False
        )
        
        embed.set_footer(text=f"Prefix: {Config.BOT_PREFIX} | Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="info")
    @commands.cooldown(1, Config.COOLDOWNS['default'], commands.BucketType.user)
    async def info(self, ctx):
        """Show bot information and statistics."""
        uptime = time.time() - self.start_time
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(
            title="🤖 Bot Information",
            color=Config.EMBED_COLORS['info']
        )
        
        embed.add_field(
            name="📊 Statistics",
            value=f"**Servers:** {len(self.bot.guilds)}\n"
                  f"**Users:** {len(self.bot.users)}\n"
                  f"**Commands:** {len(self.bot.commands)}",
            inline=True
        )
        
        embed.add_field(
            name="⚙️ Technical",
            value=f"**Python:** {platform.python_version()}\n"
                  f"**Discord.py:** {discord.__version__}\n"
                  f"**Uptime:** {int(hours)}h {int(minutes)}m {int(seconds)}s",
            inline=True
        )
        
        embed.add_field(
            name="💻 System",
            value=f"**CPU:** {psutil.cpu_percent()}%\n"
                  f"**Memory:** {psutil.virtual_memory().percent}%\n"
                  f"**Platform:** {platform.system()}",
            inline=True
        )
        
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="userinfo")
    @commands.cooldown(1, Config.COOLDOWNS['default'], commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        """Show information about a user."""
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"👤 User Information",
            color=member.color if member.color != discord.Color.default() else Config.EMBED_COLORS['info']
        )
        
        embed.add_field(
            name="📝 Basic Info",
            value=f"**Name:** {member.display_name}\n"
                  f"**ID:** {member.id}\n"
                  f"**Created:** {member.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            inline=True
        )
        
        embed.add_field(
            name="🎭 Server Info",
            value=f"**Joined:** {member.joined_at.strftime('%Y-%m-%d %H:%M:%S') if member.joined_at else 'Unknown'}\n"
                  f"**Top Role:** {member.top_role.mention}\n"
                  f"**Color:** {str(member.color)}",
            inline=True
        )
        
        embed.add_field(
            name="🔐 Permissions",
            value=f"**Administrator:** {'Yes' if member.guild_permissions.administrator else 'No'}\n"
                  f"**Manage Messages:** {'Yes' if member.guild_permissions.manage_messages else 'No'}\n"
                  f"**Kick Members:** {'Yes' if member.guild_permissions.kick_members else 'No'}",
            inline=True
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Set up the cog."""
    await bot.add_cog(General(bot)) 