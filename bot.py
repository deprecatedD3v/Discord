import discord
from discord.ext import commands
import asyncio
import logging
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    """Main Discord bot class."""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=Config.BOT_PREFIX,
            intents=intents,
            help_command=None
        )
        
        self.config = Config()
        self.initial_extensions = [
            'cogs.general',
            'cogs.admin',
            'cogs.fun',
            'cogs.events',
            'cogs.roles'
        ]
    
    async def setup_hook(self):
        """Set up the bot when it starts."""
        logger.info("Setting up bot...")
        
        # Load all extensions
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                logger.info(f"Loaded extension: {extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}: {e}")
        
        logger.info("Bot setup complete!")
    
    async def on_ready(self):
        """Event triggered when the bot is ready."""
        logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        logger.info(f"Bot is in {len(self.guilds)} guilds")
        
        # Set bot status
        activity = discord.Game(name=Config.BOT_STATUS)
        await self.change_presence(activity=activity)
        
        logger.info("Bot is ready!")
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        
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
        
        # Log unexpected errors
        logger.error(f"Unexpected error in command {ctx.command}: {error}")
        
        embed = discord.Embed(
            title="❌ Error",
            description="An unexpected error occurred. Please try again later.",
            color=Config.EMBED_COLORS['error']
        )
        await ctx.send(embed=embed)

async def main():
    """Main function to run the bot."""
    if not Config.DISCORD_TOKEN:
        logger.error("No Discord token found! Please set DISCORD_TOKEN in your environment variables.")
        return
    
    bot = DiscordBot()
    
    try:
        await bot.start(Config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested...")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main()) 