import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Discord bot."""
    
    # Discord Bot Token
    DISCORD_TOKEN = 'yourtokeMTM4MTQ1NzQ3MzU3MDg2NTI3NA.GEOen4.Zt2N_zMyvgn-p6quaaYpI4ZqxaEH5UHhSiyJAU'
    # Guild ID (optional, for guild-specific commands)
    DISCORD_GUILD_ID = '1380991263800557648'
    
    # Bot Settings
    BOT_PREFIX = os.getenv('BOT_PREFIX', '!')
    BOT_STATUS = os.getenv('BOT_STATUS', 'Playing with Discord.py')
    
    # Colors for embeds
    EMBED_COLORS = {
        'success': 0x00ff00,  # Green
        'error': 0xff0000,    # Red
        'info': 0x0099ff,     # Blue
        'warning': 0xffff00   # Yellow
    }
    
    # Command cooldowns (in seconds)
    COOLDOWNS = {
        'default': 3,
        'admin': 1,
        'fun': 5
    } 