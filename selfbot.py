"""
    TOOL_NAMEv1.0.0 by Paintilya
    versioning: vA.B.C
        A: Major changes
        B: New features
        C: Bug fixes
    Self-bots are not allowed on Discord. Use this at your own risk.
"""
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
            raise subprocess.CalledProcessError(
                cmd='pip install -r requirements.txt',
                returncode=exit_code_requirements_install,
                output='Unable to install dependencies from requirements.txt'
            )
    except subprocess.CalledProcessError as e:
        print(f"{e}\n{e.output}")
        print("Try running from the current working directory")
        sys.exit()

# Handle CTRL-C exit
def keyboard_interrupt_handler(signal, frame):
    print(f"{Fore.RED}{Style.BRIGHT}bye!{Style.RESET_ALL}")
    sys.exit(1)
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('USER_TOKEN')
PREFIX = os.getenv('PREFIX')

# Global current_theme variable because client.settings.edit doesn't seem to update it locally
current_theme = None

client = commands.Bot(command_prefix=PREFIX, self_bot=True)

@client.event
async def on_ready():
    global current_theme
    current_theme = client.settings.theme
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
    global current_theme

    match current_theme:
        case discord.Theme.light:
            try:
                current_theme = discord.Theme.dark
                await client.settings.edit(theme=discord.Theme.dark)
            except:
                await ctx.send("Something went wrong.")
            finally:
                return
        
        case discord.Theme.dark:
            try:
                current_theme = discord.Theme.light
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
 (       (    (                )          
 )\ )    )\ ) )\ )       (  ( /(   *   )  
(()/((  (()/((()/(     ( )\ )\())` )  /(  
 /(_))\  /(_))/(_))___ )((_|(_)\  ( )(_)) 
(_))((_)(_)) (_))_|___((_)_  ((_)(_(_())  
/ __| __| |  | |_      | _ )/ _ \|_   _|  
\__ \ _|| |__| __|     | _ \ (_) | | |    
|___/___|____|_|       |___/\___/  |_|    \n{Style.RESET_ALL}"""
    )
    print(f"\n{'='*75}\n")
    client.run(TOKEN)