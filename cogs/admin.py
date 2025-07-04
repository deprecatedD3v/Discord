import discord
from discord.ext import commands
from config import Config
import asyncio
from datetime import datetime, timedelta

class Admin(commands.Cog):
    """Administrative and moderation commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a member from the server."""
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot kick yourself!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot kick someone with a higher or equal role!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        try:
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title="👢 Member Kicked",
                description=f"**{member.display_name}** has been kicked from the server.",
                color=Config.EMBED_COLORS['success']
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Kicked by", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Error",
                description="I don't have permission to kick this member!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
    
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a member from the server."""
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot ban yourself!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot ban someone with a higher or equal role!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        try:
            await member.ban(reason=reason)
            
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"**{member.display_name}** has been banned from the server.",
                color=Config.EMBED_COLORS['success']
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Banned by", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Error",
                description="I don't have permission to ban this member!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
    
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def unban(self, ctx, user_id: int, *, reason="No reason provided"):
        """Unban a user by their ID."""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            
            embed = discord.Embed(
                title="🔓 User Unbanned",
                description=f"**{user.display_name}** has been unbanned from the server.",
                color=Config.EMBED_COLORS['success']
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Unbanned by", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {user.id}")
            
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            embed = discord.Embed(
                title="❌ Error",
                description="User not found or not banned!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Error",
                description="I don't have permission to unban this user!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
    
    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def clear(self, ctx, amount: int = 10):
        """Clear a specified number of messages."""
        if amount < 1 or amount > 100:
            embed = discord.Embed(
                title="❌ Error",
                description="Please specify a number between 1 and 100!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
            
            embed = discord.Embed(
                title="🧹 Messages Cleared",
                description=f"Successfully deleted **{len(deleted) - 1}** messages.",
                color=Config.EMBED_COLORS['success']
            )
            embed.set_footer(text=f"Cleared by {ctx.author.display_name}")
            
            message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Error",
                description="I don't have permission to delete messages!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
    
    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member, duration: str = "10m", *, reason="No reason provided"):
        """Mute a member for a specified duration."""
        if member == ctx.author:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot mute yourself!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="❌ Error",
                description="You cannot mute someone with a higher or equal role!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        # Parse duration
        duration_seconds = self.parse_duration(duration)
        if duration_seconds is None:
            embed = discord.Embed(
                title="❌ Error",
                description="Invalid duration format! Use: 30s, 5m, 2h, 1d",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        # Find or create muted role
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(
                    name="Muted",
                    color=discord.Color.dark_grey(),
                    reason="Mute command usage"
                )
                
                # Set permissions for all channels
                for channel in ctx.guild.channels:
                    if isinstance(channel, discord.TextChannel):
                        await channel.set_permissions(muted_role, send_messages=False)
                    elif isinstance(channel, discord.VoiceChannel):
                        await channel.set_permissions(muted_role, speak=False)
                        
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Error",
                    description="I don't have permission to create the Muted role!",
                    color=Config.EMBED_COLORS['error']
                )
                await ctx.send(embed=embed)
                return
        
        try:
            await member.add_roles(muted_role, reason=reason)
            
            embed = discord.Embed(
                title="🔇 Member Muted",
                description=f"**{member.display_name}** has been muted for **{duration}**.",
                color=Config.EMBED_COLORS['success']
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Muted by", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
            
            # Schedule unmute
            await asyncio.sleep(duration_seconds)
            if muted_role in member.roles:
                await member.remove_roles(muted_role, reason="Mute duration expired")
                
                embed = discord.Embed(
                    title="🔊 Member Unmuted",
                    description=f"**{member.display_name}** has been automatically unmuted.",
                    color=Config.EMBED_COLORS['info']
                )
                await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Error",
                description="I don't have permission to mute this member!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
    
    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Unmute a member."""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role or muted_role not in member.roles:
            embed = discord.Embed(
                title="❌ Error",
                description="This member is not muted!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        
        try:
            await member.remove_roles(muted_role, reason=reason)
            
            embed = discord.Embed(
                title="🔊 Member Unmuted",
                description=f"**{member.display_name}** has been unmuted.",
                color=Config.EMBED_COLORS['success']
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Unmuted by", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Error",
                description="I don't have permission to unmute this member!",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
    
    def parse_duration(self, duration_str):
        """Parse duration string to seconds."""
        try:
            unit = duration_str[-1].lower()
            value = int(duration_str[:-1])
            
            if unit == 's':
                return value
            elif unit == 'm':
                return value * 60
            elif unit == 'h':
                return value * 3600
            elif unit == 'd':
                return value * 86400
            else:
                return None
        except (ValueError, IndexError):
            return None

async def setup(bot):
    """Set up the cog."""
    await bot.add_cog(Admin(bot)) 