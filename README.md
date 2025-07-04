# Discord Bot Sample Project

A complete sample Discord bot built with Python and discord.py, featuring modular cogs, admin/moderation, fun commands, and event handling.

## Features
- Modular cog structure (general, admin, fun, events)
- Command cooldowns and error handling
- Moderation: kick, ban, mute, clear, unban
- Fun: 8ball, roll dice, coinflip, jokes
- Utility: ping, info, userinfo, help
- Welcome/goodbye messages
- Logging to file and console

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**
   - Copy `env_example.txt` to `.env` and fill in your Discord bot token and settings.

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Environment Variables
See `env_example.txt` for required variables:
- `DISCORD_TOKEN`: Your Discord bot token
- `DISCORD_GUILD_ID`: (Optional) Your server's guild ID
- `BOT_PREFIX`: Command prefix (default: `!`)
- `BOT_STATUS`: Status message for the bot

## Project Structure
```
.
├── bot.py            # Main bot runner
├── config.py         # Configuration and environment loading
├── requirements.txt  # Python dependencies
├── env_example.txt   # Example environment variables
├── cogs/             # Modular command/event cogs
│   ├── __init__.py
│   ├── general.py
│   ├── admin.py
│   ├── fun.py
│   └── events.py
└── README.md         # This file
```

## Notes
- Make sure your bot has the necessary permissions in your Discord server.
- For muting, the bot will create a `Muted` role if it doesn't exist.
- You can extend the bot by adding more cogs in the `cogs/` directory.

---

Enjoy your new Discord bot! 🎉
