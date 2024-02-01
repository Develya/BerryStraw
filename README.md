![BerryStraw](/res/logo2.png)

⚠️ Self-bots are not allowed on Discord. Use this at your own risks.
## About
BerryStraw is a self-bot python tool that allows you to add your own commands, to trigger any code. For example, you could control your home smart lights through Discord.
See the `Extensions` section for more information.

# Web UI
![WEB interface settings](/res/web_settings.png)
![WEB interface running](/res/web_running.png)

## Base features
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
Code your own extensions from the template located at `extensions/example.py`. BerryStraw will automatically detect it and load it.
