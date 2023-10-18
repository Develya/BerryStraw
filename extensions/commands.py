from discord.ext import commands
import discord

class Commands(commands.Cog):
    def __init__(self, client):
        self.current_discord_ui_theme = None
        self.client = client

    @commands.command()
    async def st(self, ctx):
        """
        Switch Theme command

        Toggles between dark and light themes
        """

        if self.current_discord_ui_theme == None:
            self.current_discord_ui_theme = self.client.settings.theme

        match self.current_discord_ui_theme:
            case discord.Theme.light:
                try:
                    self.current_discord_ui_theme = discord.Theme.dark
                    await self.client.settings.edit(theme=discord.Theme.dark)
                except:
                    await ctx.send("Something went wrong.")
                finally:
                    return
            
            case discord.Theme.dark:
                try:
                    self.current_discord_ui_theme = discord.Theme.light
                    await self.client.settings.edit(theme=discord.Theme.light)
                except:
                    await ctx.send("Something went wrong.")
                finally:
                    return
            
            case _:
                await ctx.send("Something went wrong.")
                return


async def setup(client):
    await client.add_cog(Commands(client))