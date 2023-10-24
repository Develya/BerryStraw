![BerryStraw](../BerryStraw/res/logo2.png)

⚠️ Self-bots are not allowed on Discord. Use this at your own risks.
## About
BerryStraw is a self-bot python tool that gives you access to multiple commands to make your Discord experience a little more fun and easy. 
You can also code your own extensions to add custom features or even manage stuff outside of Discord . See the `Extensions` section for more information.

# Web UI
![WEB interface settings](../BerryStraw/res/web_settings.png)
![WEB interface running](../BerryStraw/res/web_running.png)

## Current features
- (st) Switch theme: toggle between light and dark theme.

## Requirements
- Python 3.10 or higher
- Discord.py must not be installed in the environment
- See requirements.txt for third-party modules requirements

## Installation & Usage
1. Clone this repository.
2. `pip install streamlit`
3. Run `python -m streamlit run web.py --server.address=127.0.0.1` from the current working directory.

## Extensions
Code your own extensions from the template located at `extensions/example.py`. BerryStraw will automatically detect it and load it. You can make custom commands to run stuff on or outside Discord. Example: a command to manage your home smart lights from discord commands.