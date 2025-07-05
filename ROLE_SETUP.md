# Role Management System Setup Guide

## Overview
This Discord bot includes a comprehensive role management system with categorized roles organized as requested:

### Role Categories

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

## Setup Instructions

### 1. Bot Permissions
Make sure your bot has the following permissions:
- `Manage Roles` - To create, assign, and remove roles
- `Send Messages` - To send role management messages
- `Use Slash Commands` - For interactive buttons
- `Embed Links` - To send formatted role information

### 2. Creating Roles
1. Run the command: `!createroles`
2. This will create all the roles in the categories above
3. The bot will show you which roles were created successfully

### 3. Using the Role System
1. Users can run `!roles` to see all available role categories
2. Click on a category button to see the roles in that category
3. Click on individual role buttons to add/remove that role
4. Use the "Back to Categories" button to return to the main menu

## Commands

### User Commands
- `!roles` - Show role categories and manage roles

### Admin Commands
- `!createroles` - Create all role categories and roles
- `!deleteroles` - Delete all bot-created roles (with confirmation)

## Features

- **Interactive Buttons**: Users can click buttons to manage their roles
- **Category Organization**: Roles are organized into logical categories
- **Toggle Functionality**: Click a role button to add/remove the role
- **Permission Checks**: Bot checks for proper permissions before actions
- **Error Handling**: Graceful error messages for various scenarios
- **Confirmation Dialogs**: Admin commands include confirmation steps

## Notes

- Roles are created with default colors (can be customized by admins later)
- Users can have multiple roles from different categories
- The system prevents duplicate role assignments
- All role changes are logged with reasons for audit purposes 