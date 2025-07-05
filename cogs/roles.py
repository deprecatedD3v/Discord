import discord
from discord.ext import commands
from config import Config
import asyncio

class Roles(commands.Cog):
    """Role management commands with categorized roles."""
    
    def __init__(self, bot):
        self.bot = bot
        
        # Define role categories
        self.role_categories = {
            "tuar_games": {
                "name": "🎮 Tuar Studios Games",
                "description": "Stay updated with Tuar Studios games and testing",
                "roles": ["📰 News", "🧪 Tester"]
            },
            "platforms": {
                "name": "💻 Platforms",
                "description": "Choose your gaming platform",
                "roles": ["🖥️ PC", "🎮 Console", "📱 Mobile"]
            },
            "regions": {
                "name": "🌍 Regions",
                "description": "Select your region",
                "roles": ["🇪🇺 EU", "🇺🇸 NA East", "🇺🇸 NA West", "🇦🇺 Oceania", "🌏 Asia", "🇿🇦 South Africa", "🇧🇷 South America"]
            }
        }
    
    @commands.command(name="roles")
    @commands.cooldown(1, Config.COOLDOWNS['default'], commands.BucketType.user)
    async def show_roles(self, ctx):
        """Show all available role categories."""
        embed = discord.Embed(
            title="🎭 Role Categories",
            description="Click the buttons below to manage your roles in each category:",
            color=Config.EMBED_COLORS['info']
        )
        
        for category_id, category in self.role_categories.items():
            embed.add_field(
                name=category["name"],
                value=f"{category['description']}\nRoles: {', '.join(category['roles'])}",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        
        # Create buttons for each category
        view = RoleCategoryView(self.role_categories, self.bot)
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name="createroles")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def create_roles(self, ctx):
        """Create all role categories and roles (Admin only)."""
        embed = discord.Embed(
            title="⚙️ Creating Roles",
            description="Creating role categories and roles...",
            color=Config.EMBED_COLORS['info']
        )
        message = await ctx.send(embed=embed)
        
        created_roles = []
        failed_roles = []
        
        # Create roles for each category
        for category_id, category in self.role_categories.items():
            for role_name in category["roles"]:
                try:
                    # Check if role already exists
                    existing_role = discord.utils.get(ctx.guild.roles, name=role_name)
                    if existing_role:
                        created_roles.append(f"✅ {role_name} (already exists)")
                        continue
                    
                    # Create the role
                    role = await ctx.guild.create_role(
                        name=role_name,
                        color=discord.Color.default(),
                        reason=f"Role creation by {ctx.author.display_name}"
                    )
                    created_roles.append(f"✅ {role_name}")
                    
                except discord.Forbidden:
                    failed_roles.append(f"❌ {role_name} (no permission)")
                except Exception as e:
                    failed_roles.append(f"❌ {role_name} (error: {str(e)})")
        
        # Update the embed with results
        result_embed = discord.Embed(
            title="🎭 Role Creation Complete",
            color=Config.EMBED_COLORS['success'] if not failed_roles else Config.EMBED_COLORS['warning']
        )
        
        if created_roles:
            result_embed.add_field(
                name="✅ Created/Existing Roles",
                value="\n".join(created_roles),
                inline=False
            )
        
        if failed_roles:
            result_embed.add_field(
                name="❌ Failed Roles",
                value="\n".join(failed_roles),
                inline=False
            )
        
        result_embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await message.edit(embed=result_embed)
    
    @commands.command(name="deleteroles")
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, Config.COOLDOWNS['admin'], commands.BucketType.user)
    async def delete_roles(self, ctx):
        """Delete all bot-created roles (Admin only)."""
        embed = discord.Embed(
            title="🗑️ Deleting Roles",
            description="Are you sure you want to delete all bot-created roles?",
            color=Config.EMBED_COLORS['warning']
        )
        embed.add_field(
            name="⚠️ Warning",
            value="This action cannot be undone!",
            inline=False
        )
        
        # Create confirmation view
        view = RoleDeletionConfirmationView(self.role_categories, self.bot)
        await ctx.send(embed=embed, view=view)

class RoleCategoryView(discord.ui.View):
    """View for role category selection."""
    
    def __init__(self, role_categories, bot):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.role_categories = role_categories
        self.bot = bot
    
    @discord.ui.button(label="🎮 Tuar Studios Games", style=discord.ButtonStyle.primary, custom_id="tuar_games")
    async def tuar_games_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_category_roles(interaction, "tuar_games")
    
    @discord.ui.button(label="💻 Platforms", style=discord.ButtonStyle.primary, custom_id="platforms")
    async def platforms_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_category_roles(interaction, "platforms")
    
    @discord.ui.button(label="🌍 Regions", style=discord.ButtonStyle.primary, custom_id="regions")
    async def regions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_category_roles(interaction, "regions")
    
    async def show_category_roles(self, interaction: discord.Interaction, category_id: str):
        """Show roles for a specific category."""
        category = self.role_categories[category_id]
        
        embed = discord.Embed(
            title=category["name"],
            description=category["description"],
            color=Config.EMBED_COLORS['info']
        )
        
        # Create role selection view
        view = RoleSelectionView(category["roles"], category_id, self.bot)
        
        await interaction.response.edit_message(embed=embed, view=view)

class RoleSelectionView(discord.ui.View):
    """View for role selection within a category."""
    
    def __init__(self, roles, category_id, bot):
        super().__init__(timeout=300)  # 5 minutes timeout
        self.roles = roles
        self.category_id = category_id
        self.bot = bot
        
        # Add buttons for each role
        for role_name in roles:
            button = discord.ui.Button(
                label=role_name,
                style=discord.ButtonStyle.secondary,
                custom_id=f"role_{role_name.lower().replace(' ', '_')}"
            )
            button.callback = self.create_role_callback(role_name)
            self.add_item(button)
        
        # Add back button
        back_button = discord.ui.Button(
            label="⬅️ Back to Categories",
            style=discord.ButtonStyle.danger,
            custom_id="back_to_categories"
        )
        back_button.callback = self.back_to_categories
        self.add_item(back_button)
    
    def create_role_callback(self, role_name):
        """Create a callback function for a specific role."""
        async def role_callback(interaction: discord.Interaction):
            await self.toggle_role(interaction, role_name)
        return role_callback
    
    async def toggle_role(self, interaction: discord.Interaction, role_name: str):
        """Toggle a role for the user."""
        member = interaction.user
        guild = interaction.guild
        
        # Find the role
        role = discord.utils.get(guild.roles, name=role_name)
        
        if not role:
            embed = discord.Embed(
                title="❌ Role Not Found",
                description=f"The role '{role_name}' doesn't exist. Please ask an administrator to create it.",
                color=Config.EMBED_COLORS['error']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if user has the role
        has_role = role in member.roles
        
        try:
            if has_role:
                # Remove the role
                await member.remove_roles(role, reason=f"Role removal via bot by {member.display_name}")
                action = "removed"
                color = Config.EMBED_COLORS['warning']
            else:
                # Add the role
                await member.add_roles(role, reason=f"Role assignment via bot by {member.display_name}")
                action = "added"
                color = Config.EMBED_COLORS['success']
            
            embed = discord.Embed(
                title="✅ Role Updated",
                description=f"The role **{role_name}** has been {action} for you.",
                color=color
            )
            embed.set_footer(text=f"Requested by {member.display_name}")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Error",
                description="I don't have permission to manage roles!",
                color=Config.EMBED_COLORS['error']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"An error occurred: {str(e)}",
                color=Config.EMBED_COLORS['error']
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def back_to_categories(self, interaction: discord.Interaction):
        """Go back to the category selection."""
        embed = discord.Embed(
            title="🎭 Role Categories",
            description="Click the buttons below to manage your roles in each category:",
            color=Config.EMBED_COLORS['info']
        )
        
        role_categories = {
            "tuar_games": {
                "name": "🎮 Tuar Studios Games",
                "description": "Stay updated with Tuar Studios games and testing",
                "roles": ["📰 News", "🧪 Tester"]
            },
            "platforms": {
                "name": "💻 Platforms",
                "description": "Choose your gaming platform",
                "roles": ["🖥️ PC", "🎮 Console", "📱 Mobile"]
            },
            "regions": {
                "name": "🌍 Regions",
                "description": "Select your region",
                "roles": ["🇪🇺 EU", "🇺🇸 NA East", "🇺🇸 NA West", "🇦🇺 Oceania", "🌏 Asia", "🇿🇦 South Africa", "🇧🇷 South America"]
            }
        }
        
        for category_id, category in role_categories.items():
            embed.add_field(
                name=category["name"],
                value=f"{category['description']}\nRoles: {', '.join(category['roles'])}",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        
        # Create buttons for each category
        view = RoleCategoryView(role_categories, self.bot)
        await interaction.response.edit_message(embed=embed, view=view)

class RoleDeletionConfirmationView(discord.ui.View):
    """View for role deletion confirmation."""
    
    def __init__(self, role_categories, bot):
        super().__init__(timeout=60)  # 1 minute timeout
        self.role_categories = role_categories
        self.bot = bot
    
    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm role deletion."""
        embed = discord.Embed(
            title="🗑️ Deleting Roles",
            description="Deleting all bot-created roles...",
            color=Config.EMBED_COLORS['warning']
        )
        await interaction.response.edit_message(embed=embed, view=None)
        
        deleted_roles = []
        failed_roles = []
        
        # Delete roles for each category
        for category_id, category in self.role_categories.items():
            for role_name in category["roles"]:
                try:
                    role = discord.utils.get(interaction.guild.roles, name=role_name)
                    if role:
                        await role.delete(reason=f"Role deletion by {interaction.user.display_name}")
                        deleted_roles.append(f"✅ {role_name}")
                    else:
                        deleted_roles.append(f"ℹ️ {role_name} (not found)")
                        
                except discord.Forbidden:
                    failed_roles.append(f"❌ {role_name} (not found)")
                except Exception as e:
                    failed_roles.append(f"❌ {role_name} (error: {str(e)})")
        
        # Update the embed with results
        result_embed = discord.Embed(
            title="🎭 Role Deletion Complete",
            color=Config.EMBED_COLORS['success'] if not failed_roles else Config.EMBED_COLORS['warning']
        )
        
        if deleted_roles:
            result_embed.add_field(
                name="✅ Deleted/Not Found Roles",
                value="\n".join(deleted_roles),
                inline=False
            )
        
        if failed_roles:
            result_embed.add_field(
                name="❌ Failed Roles",
                value="\n".join(failed_roles),
                inline=False
            )
        
        result_embed.set_footer(text=f"Requested by {interaction.user.display_name}")
        await interaction.message.edit(embed=result_embed)
    
    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel role deletion."""
        embed = discord.Embed(
            title="❌ Cancelled",
            description="Role deletion has been cancelled.",
            color=Config.EMBED_COLORS['info']
        )
        await interaction.response.edit_message(embed=embed, view=None)

async def setup(bot):
    """Set up the cog."""
    await bot.add_cog(Roles(bot)) 