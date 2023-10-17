"""
    BerryStraw v1.0.2 by Paintilya
    Self-bots are not allowed on Discord. Use this at your own risk.
"""
# Builtin dependencies
import os
import json
import sys
import signal
import subprocess

try: # dependencies that need to be installed
    from dotenv import load_dotenv
    import discord
    from discord.ext import commands
    import requests
    import colorama
    from colorama import Fore, Style
except ImportError: # Install dependencies if they are not installed
    try:
        exit_code_requirements_install = os.system('pip install -r requirements.txt')
        if exit_code_requirements_install == 0:
            from dotenv import load_dotenv
            from discord.ext import commands
            import discord
            import requests
        else: 
            # If installation fails - probably because the tool
            # was not ran in the current working directory
            raise subprocess.CalledProcessError(
                cmd='pip install -r requirements.txt',
                returncode=exit_code_requirements_install,
                output='Unable to install dependencies from requirements.txt'
            )
    except subprocess.CalledProcessError as e:
        print(f"{e}\n{e.output}")
        print("Try running from the current working directory")
        sys.exit(1)

# Handle CTRL-C exit
def keyboard_interrupt_handler(signal, frame):
    print(f"{Fore.RED}{Style.BRIGHT}bye!{Style.RESET_ALL}")
    sys.exit(0)
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

# Load .env configuration
load_dotenv()
TOKEN = os.getenv('USER_TOKEN')
PREFIX = os.getenv('PREFIX')

# Global current_theme variable because client.settings.edit() doesn't seem to update it locally
current_discord_ui_theme = None

client = commands.Bot(command_prefix=PREFIX, self_bot=True)

@client.event
async def on_ready():
    global current_discord_ui_theme
    current_discord_ui_theme = client.settings.theme
    print(f"\n{'='*75}\n")
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Logged in as {client.user}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}Listening to commands...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}Prefix: '{PREFIX}'{Style.RESET_ALL}")

@client.command()
async def st(ctx):
    """
    Switch Theme command

    toggles between dark and light themes
    """
    global current_discord_ui_theme

    match current_discord_ui_theme:
        case discord.Theme.light:
            try:
                current_discord_ui_theme = discord.Theme.dark
                await client.settings.edit(theme=discord.Theme.dark)
            except:
                await ctx.send("Something went wrong.")
            finally:
                return
        
        case discord.Theme.dark:
            try:
                current_discord_ui_theme = discord.Theme.light
                await client.settings.edit(theme=discord.Theme.light)
            except:
                await ctx.send("Something went wrong.")
            finally:
                return
        
        case _:
            await ctx.send("Something went wrong.")
            return

if __name__ == "__main__":
    print(
        f"""{Fore.RED}{Style.BRIGHT}
______ ___________________   _______ ___________  ___  _    _ 
| ___ \  ___| ___ \ ___ \ \ / /  ___|_   _| ___ \/ _ \| |  | |
| |_/ / |__ | |_/ / |_/ /\ V /\ `--.  | | | |_/ / /_\ \ |  | |
| ___ \  __||    /|    /  \ /  `--. \ | | |    /|  _  | |/\| |
| |_/ / |___| |\ \| |\ \  | | /\__/ / | | | |\ \| | | \  /\  /
\____/\____/\_| \_\_| \_| \_/ \____/  \_/ \_| \_\_| |_/\/  \/  \n{Style.RESET_ALL}"""
    )
    print(f"\n{'='*75}\n")
    try:
        client.run(TOKEN)
    except (discord.errors.LoginFailure, discord.errors.ConnectionClosed) as e:
        print(f"\n{e}\nExiting.")
        sys.exit(1)
    