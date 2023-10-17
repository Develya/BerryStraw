"""
    BerryStraw v2.1.0 by Paintilya
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
            import discord
            from discord.ext import commands
            import requests
            import colorama
            from colorama import Fore, Style
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

client = commands.Bot(command_prefix=PREFIX, self_bot=True)

async def load_bot_extensions(): # Dynamically detects extensions and loads them
    print(f"{Fore.GREEN}{Style.DIM}Loading extensions...{Style.RESET_ALL}")

    for extension in [f for f in os.listdir('./extensions') if f.endswith('.py')]:
        try:
            extension = extension.replace('.py', '')
            await client.load_extension(f"extensions.{extension}")
            print(f"{Fore.GREEN}{Style.DIM}Loaded {extension}{Style.RESET_ALL}")
        except (
            discord.ext.commands.ExtensionNotFound,
            discord.ext.commands.ExtensionAlreadyLoaded,
            discord.ext.commands.NoEntryPointError,
            discord.ext.commands.ExtensionFailed
        ) as e:
            print(f"{Fore.RED}Error loading {extension}: {e}{Style.RESET_ALL}")

@client.event
async def on_ready():
    global current_discord_ui_theme
    current_discord_ui_theme = client.settings.theme
    print(f"\n{'='*75}\n")
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Logged in as {client.user}{Style.RESET_ALL}")

    await load_bot_extensions()

    print(f"{Fore.GREEN}{Style.BRIGHT}Ready!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}Prefix: '{PREFIX}'{Style.RESET_ALL}")


if __name__ == "__main__":
    print(
        f"""{Fore.RED}{Style.BRIGHT}
______ ___________________   _______ ___________  ___  _    _ 
| ___ \  ___| ___ \ ___ \ \ / /  ___|_   _| ___ \/ _ \| |  | |
| |_/ / |__ | |_/ / |_/ /\ V /\ `--.  | | | |_/ / /_\ \ |  | |
| ___ \  __||    /|    /  \ /  `--. \ | | |    /|  _  | |/\| |
| |_/ / |___| |\ \| |\ \  | | /\__/ / | | | |\ \| | | \  /\  /
\____/\____/\_| \_\_| \_| \_/ \____/  \_/ \_| \_\_| |_/\/  \/  \n v2.1.0{Style.RESET_ALL}"""
    )
    print(f"\n{'='*75}\n")
    try:
        client.run(TOKEN)
    except (discord.errors.LoginFailure, discord.errors.ConnectionClosed) as e:
        print(f"\n{e}\nExiting.")
        sys.exit(1)
