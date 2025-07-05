# Discord Bot

A Discord bot built with discord.py featuring role management and moderation tools.

## Features

- **Role Management System**: Interactive role categories with emojis
- **Moderation Tools**: Kick, ban, mute, and clear commands
- **Fun Commands**: 8ball, dice rolling, coin flip, and jokes
- **General Utilities**: Ping, user info, and bot statistics

## Role Categories

1. **🎮 Tuar Studios Games**
   - 📰 News
   - 🧪 Tester

2. **💻 Platforms**
   - 🖥️ PC
   - 🎮 Console
   - 📱 Mobile

3. **🌍 Regions**
   - 🇪🇺 EU
   - 🇺🇸 NA East
   - 🇺🇸 NA West
   - 🇦🇺 Oceania
   - 🌏 Asia
   - 🇿🇦 South Africa
   - 🇧🇷 South America

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure your bot token in `config.py`
3. Run the bot: `python bot.py`

## Commands

- `!help` - Show all available commands
- `!roles` - Manage your roles
- `!createroles` - Create all role categories (admin only)
- `!deleteroles` - Delete all bot-created roles (admin only)

## Git Integration

This project is connected to GitHub and can be deployed directly to VPS for real-time updates.

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
