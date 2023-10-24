"""
Web GUI

run with:                   
python -m streamlit run web.py --server.address=127.0.0.1

--server.address=127.0.0.1 => makes it only available on your device for security
"""

# Builtin dependencies
import os
import sys
import subprocess
import signal
import asyncio
import time
import json

try: # dependencies that need to be installed
    from dotenv import load_dotenv, find_dotenv, set_key
    import streamlit as st
    import psutil
except ImportError: # Install dependencies if they are not installed
    try:
        exit_code_requirements_install = os.system('pip install -r requirements.txt')
        if exit_code_requirements_install == 0:
            from dotenv import load_dotenv
            import streamlit as st
            import psutil
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
        sys.exit(1)

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)
VERSION = None
TOKEN = os.getenv('USER_TOKEN')
PREFIX = os.getenv('PREFIX')
stop_checking_status = False
with open('info.json', 'r') as f:
    info_json = json.load(f)
    VERSION = info_json['version']

@st.cache_resource
def reset_state():
    with open('state.json', 'w') as f:
        json_state = {
            'berrystraw_state': 'waiting',
            'berrystraw_subprocess_pid': None,
            'error_message': None
        }
        json.dump(json_state, f)
    return json_state
reset_state()
###
# STATE CONTROL
###
def save_state():
    with open('state.json', 'w') as f:
        json_state = {
            'berrystraw_state': st.session_state['berrystraw_state'],
            'berrystraw_subprocess_pid': st.session_state['berrystraw_subprocess_pid'],
            'error_message': st.session_state['error_message']
        }
        json.dump(json_state, f)
###
# STATE CONTROL
###

###
# BERRYSTRAW CONTROL
###
def launch_berrystraw():
    st.session_state['berrystraw_subprocess_pid'] = subprocess.Popen(['python', 'berrystraw.py']).pid
    st.session_state['berrystraw_state'] = 'running'
    st.session_state['berrystraw_subprocess_pid'] = st.session_state['berrystraw_subprocess_pid']
    save_state()
    st.rerun()

def terminate_berrystraw():
    global stop_checking_status
    stop_checking_status = True
    os.kill(st.session_state['berrystraw_subprocess_pid'], signal.SIGTERM)
    st.session_state['berrystraw_state'] = 'waiting'
    st.session_state['berrystraw_subprocess_pid'] = None
    save_state()
    st.rerun()

def check_status():
    try:
        global stop_checking_status
        while st.session_state['berrystraw_state'] == 'running' and stop_checking_status is False:
            try:
                psutil.Process(st.session_state.berrystraw_subprocess_pid)
            except psutil.NoSuchProcess:
                st.session_state['berrystraw_state'] = 'error'
                st.session_state['error_message'] = 'BerryStraw encountered an error. Check console for troubleshooting.'
                save_state()
                st.rerun()
            time.sleep(1)
        stop_checking_status = False
        return
    except KeyError:
        return
###
# BERRYSTRAW CONTROL
###

###
# SETTINGS CONTROL
###
def set_setting(key, value):
    global dotenv_file
    set_key(dotenv_file, key, value)
###
# SETTINGS CONTROL
###

###
# VIEWS
###
def display_waiting():
    with st.expander('Settings'):
        display_settings()
    launch_button = st.button('▶ Launch')
    if launch_button:
        launch_berrystraw()

def display_settings():
    token = st.text_input('Token', value=TOKEN, type='password')
    prefix = st.text_input('Prefix', value=PREFIX)
    if token:
        set_setting('USER_TOKEN', token)
    if prefix:
        set_setting('PREFIX', prefix)

def display_running():
    st.success("BerryStraw is running.")
    terminate_button = st.button('Terminate', type='primary')
    if terminate_button:
        terminate_berrystraw()
    check_status()

def display_error():
    st.warning(f"{st.session_state['error_message']}", icon='⚠️')
###
# VIEWS
###

###
# STREAMLIT
###
if 'berrystraw_state' not in st.session_state:
    with open('state.json', 'r') as f:
        old_session_state = json.load(f)
        st.session_state['berrystraw_state'] = old_session_state['berrystraw_state']
        st.session_state['berrystraw_subprocess_pid'] = old_session_state['berrystraw_subprocess_pid']
        st.session_state['error_message'] = old_session_state['error_message']

st.title(f"BerryStraw v{VERSION}")

match st.session_state.berrystraw_state:
    case 'waiting':
        display_waiting()
    case 'running':
        display_running()
    case _:
        display_error()
###
# STREAMLIT
###
