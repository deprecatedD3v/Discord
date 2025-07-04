import discord
from discord.ext import commands
from config import Config
import random

class Fun(commands.Cog):
    """Fun and entertainment commands."""
    def __init__(self, bot):
        self.bot = bot
        self.eight_ball_responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.", "You may rely on it.",
            "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
            "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]
    
    @commands.command(name="8ball")
    @commands.cooldown(1, Config.COOLDOWNS['fun'], commands.BucketType.user)
    async def eight_ball(self, ctx, *, question: str):
        """Ask the magic 8-ball a question."""
        response = random.choice(self.eight_ball_responses)
        embed = discord.Embed(
            title="🎱 8-Ball",
            description=f"**Question:** {question}\n**Answer:** {response}",
            color=Config.EMBED_COLORS['info']
        )
        await ctx.send(embed=embed)
    
    @commands.command(name="roll")
    @commands.cooldown(1, Config.COOLDOWNS['fun'], commands.BucketType.user)
    async def roll(self, ctx, dice: str = "1d6"):
        """Roll dice in NdM format (e.g., 2d6)."""
        try:
            rolls, limit = map(int, dice.lower().split('d'))
        except Exception:
            embed = discord.Embed(
                title="❌ Error",
                description="Format must be NdM (e.g., 2d6)",
                color=Config.EMBED_COLORS['error']
            )
            await ctx.send(embed=embed)
            return
        results = [random.randint(1, limit) for _ in range(rolls)]
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"Rolled {dice}: {', '.join(map(str, results))}",
            color=Config.EMBED_COLORS['info']
        )
        await ctx.send(embed=embed)
    
    @commands.command(name="coinflip")
    @commands.cooldown(1, Config.COOLDOWNS['fun'], commands.BucketType.user)
    async def coinflip(self, ctx):
        """Flip a coin."""
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"Result: **{result}**",
            color=Config.EMBED_COLORS['info']
        )
        await ctx.send(embed=embed)
    
    @commands.command(name="joke")
    @commands.cooldown(1, Config.COOLDOWNS['fun'], commands.BucketType.user)
    async def joke(self, ctx):
        """Tell a random joke."""
        jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the math book look sad? Because it had too many problems.",
            "Why did the chicken join a band? Because it had the drumsticks!",
            "Why can't you hear a pterodactyl go to the bathroom? Because the 'P' is silent!"
        ]
        joke = random.choice(jokes)
        embed = discord.Embed(
            title="😂 Joke",
            description=joke,
            color=Config.EMBED_COLORS['info']
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot)) 