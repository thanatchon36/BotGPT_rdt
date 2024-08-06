import streamlit as st
from streamlit_feedback import streamlit_feedback
import time
import datetime
import pandas as pd
from PIL import Image
import os
import csv
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import requests
from ast import literal_eval
import random

def get_response_2(message, history, cube_list = []):
    start_time = time.time()
    url = 'https://pc140032645.bot.or.th/rdt_brainstorming'
    myobj = { "prompt": message, "history": history, 'cube':  cube_list}
    result = requests.post(url, json = myobj, verify = False).json()
    execution_time = time.time() - start_time
    execution_time = round(execution_time, 2)
    result['frontend_query_time'] = execution_time
    return result
def get_response_3(message, history, cube_list = []):
    start_time = time.time()
    url = 'https://pc140032645.bot.or.th/metadata'
    myobj = { "prompt": message, "history": history, 'cube':  cube_list}
    result = requests.post(url, json = myobj, verify = False).json()
    execution_time = time.time() - start_time
    execution_time = round(execution_time, 2)
    result['frontend_query_time'] = execution_time
    return result
def get_response_4(message, history, cube_list = []):
    start_time = time.time()
    url = 'https://pc140032645.bot.or.th/botgpt_query_autogen'
    myobj = { "prompt": message, "history": history, 'cube':  cube_list}
    result = requests.post(url, json = myobj, verify = False).json()
    execution_time = time.time() - start_time
    execution_time = round(execution_time, 2)
    result['frontend_query_time'] = execution_time
    return result

def reset(df):
    cols = df.columns
    return df.reset_index()[cols]

show_chat_history_no = 5
admin_list = ['thanatcc', 'da']

st.set_page_config(page_title = 'BotGPT', page_icon = 'fav.png', layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login('BotGPT Login', 'main')

button_name_list = ["RDT Brainstorming",
                    "RDT Copilot - Metadata",
                    "RDT Copilot - SQL Coder",
                    ]

hidden_agent_name_list = ["cube_analyst", "information_gathering_agent", "cube_selector_assistant"]

if st.session_state["authentication_status"]:
    
    if "chat_id" not in st.session_state:
        now = str(datetime.datetime.now())
        st.session_state.chat_id  = now
        st.session_state.history = []

    bot_image = Image.open('fav.png')
    bot_image_2 = Image.open('fav_3.png')
    user_image = Image.open('fav_2.png')

    with st.sidebar:
        
        clear_session_click = st.button("New Chat")
        if clear_session_click:
            st.session_state.messages = []
            st.session_state.context = []
            now = str(datetime.datetime.now())
            st.session_state.chat_id  = now
            st.session_state.history = []

        context_radio = st.radio(
            "Task:",
            button_name_list
        )

        cube_1 = False
        cube_1_1 = False
        cube_3 = False
        cube_4 = False
        cube_5 = False
        cube_6 = False
        cube_7 = False
        cube_8 = False
        cube_8_1 = False
        cube_9 = False
        smart_cube = False

        with st.expander("Select Cube"):
            cube_1 = st.checkbox("Cube_1")
            cube_1_1 = st.checkbox("Cube_1_1")
            cube_3 = st.checkbox("Cube_3")
            cube_4 = st.checkbox("Cube_4")
            cube_5 = st.checkbox("Cube_5")
            cube_6 = st.checkbox("Cube_6")
            cube_7 = st.checkbox("Cube_7")
            cube_8 = st.checkbox("Cube_8")
            cube_8_1 = st.checkbox("Cube_8_1")
            cube_9 = st.checkbox("Cube_9")
            smart_cube = st.checkbox("Smart_cube")
        # dev_checkbox = st.checkbox('Development')
        
        csv_file = f"data/{st.session_state.username}.csv"
        file_exists = os.path.isfile(csv_file)
        if file_exists:
            if len(pd.read_csv(csv_file, sep = ',')) > 0:
                # Init State Sessioin
                if 'page' not in st.session_state:
                    st.session_state['page'] = 1
                    
                with st.expander("Chat History"):
                    hist_df = pd.read_csv(f'data/{st.session_state.username}.csv', sep = ',')
                    full_hist_df = hist_df.copy()
                    hist_df = reset(hist_df.sort_values(by = 'turn_id', ascending = False))
                    hist_df = hist_df.groupby('chat_id').first().reset_index()
                    hist_df = reset(hist_df.sort_values(by = 'turn_id', ascending = False))

                    hist_df['page'] = hist_df.index
                    hist_df['page'] = hist_df['page'] / show_chat_history_no
                    hist_df['page'] = hist_df['page'].astype(int)
                    hist_df['page'] = hist_df['page'] + 1

                    fil_hist_df = full_hist_df.copy()

                    st.session_state['max_page'] = hist_df['page'].max()

                    filter_hist_df_2 = reset(hist_df[hist_df['page'] == st.session_state['page']])

                    for index, row in filter_hist_df_2.iterrows():
                        if st.session_state.chat_id != row['chat_id']:
                            history_list = literal_eval(fil_hist_df['history'].values[-1])
                            chat_button_text = history_list[-1]['content']
                            chat_button_click = st.button(f"{chat_button_text[:30]}" + '...', key = row['chat_id'])
                            if chat_button_click:
                                st.session_state.messages = []
                                st.session_state.context = []
                                st.session_state.chat_id = row['chat_id']
                                st.session_state.turn_id = row['turn_id']
                                fil_hist_df = reset(fil_hist_df[fil_hist_df['chat_id'] == row['chat_id']])
                                history_list = literal_eval(fil_hist_df['history'].values[-1])
                                st.session_state.history = history_list
                                chat_id = fil_hist_df['chat_id'].values[-1]
                                for i, each_dict in enumerate(history_list):
                                    if 'user' in each_dict['name'].lower():
                                        st.session_state.messages.append({"role": "user", "content": each_dict['content'], "raw_content": ""})
                                        st.session_state.context.append({"role": "user", "content": ""})
                                    else:
                                        response = f"{each_dict['name']}: {each_dict['content']}"
                                        st.session_state.messages.append({"role": "assistant", "content": response, "chat_id": chat_id, "turn_id":  chat_id + '_' + str(i),
                                                                        "raw_content": "", "agent_name": each_dict['name'],
                                                                        })
                                        st.session_state.context.append({"role": "assistant", "content": ""})

                    if 'max_page' not in st.session_state:
                        st.session_state['max_page'] = 10
                    if int(st.session_state['max_page']) > 1:
                        page = st.slider('Page No:', 1, int(st.session_state['max_page']), key = 'page')

        with st.expander("Change Password"):
            try:
                if authenticator.reset_password(st.session_state["username"], 'Reset password'):
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)

        if st.session_state.username in admin_list:
            with st.expander("Register User"):
                try:
                    if authenticator.register_user('Register user', preauthorization=False):
                        with open('config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        st.success('User registered successfully')
                except Exception as e:
                    st.error(e)

        authenticator.logout(f"Logout ({st.session_state['username']})", 'main', key='unique_key')

    with st.chat_message("assistant", avatar = bot_image_2):
        # Create an empty message placeholder
        mp = st.empty()
        # Create a container for the message
        sl = mp.container()
        # Add a Markdown message describing the app
        sl.markdown(f"""
            Hi {st.session_state.name}! I am BotGPT, ready to provide assistance.
        """)

        existing_df = pd.DataFrame()

    mp = st.empty()

    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "context" not in st.session_state:
        st.session_state.context = []

    # Display chat messages from history on app rerun
    for message_i, message in enumerate(st.session_state.messages):
        if message["role"] == "assistant":
            if message['agent_name'] in hidden_agent_name_list:
                with st.expander(message['agent_name']):
                    with st.chat_message(message["role"], avatar = bot_image_2):
                        st.markdown(message["content"])
            else:
                with st.chat_message(message["role"], avatar = bot_image_2):
                    st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar = user_image):
                st.markdown(message["content"])
                
    # Check if there's a user input prompt
        # with st.chat_message("AI"):
        #     st.write("Hello 👋")
    if prompt := st.chat_input(placeholder="Kindly input your query or command for prompt assistance..."):
        Is_Human_Required = True
        if Is_Human_Required == True:
            st.chat_message("user", avatar = user_image).write(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt, "raw_content": ""})
            st.session_state.context.append({"role": "user", "content": ""})
        with st.spinner('Thinking...'):                        
            while True:
                cube_list = []
                if cube_1:
                    cube_list.append('cube_1')
                if cube_1_1:
                    cube_list.append('cube_1_1')
                if cube_3:
                    cube_list.append('cube_3')
                if cube_4:
                    cube_list.append('cube_4')
                if cube_5:
                    cube_list.append('cube_5')
                if cube_6:
                    cube_list.append('cube_6')
                if cube_7:
                    cube_list.append('cube_7')
                if cube_8:
                    cube_list.append('cube_8')
                if cube_8_1:
                    cube_list.append('cube_8_1')
                if cube_9:
                    cube_list.append('cube_9')
                if smart_cube:
                    cube_list.append('smart_cube')
                if context_radio == button_name_list[0]:
                    response_dict = get_response_2(prompt, history = st.session_state.history, cube_list = cube_list)
                elif context_radio == button_name_list[1]:
                    response_dict = get_response_3(prompt, history = st.session_state.history, cube_list = cube_list)
                elif context_radio == button_name_list[2]:
                    response_dict = get_response_4(prompt, history = st.session_state.history, cube_list = cube_list)
                response = response_dict['response']['content']
                st.session_state.history = response_dict['history']
                frontend_query_time = response_dict['frontend_query_time']
                history_list = response_dict['history']
                Is_Human_Required = response_dict['Is_Human_Required']

                agent_name = response_dict['response']['name']
                
                if agent_name in hidden_agent_name_list:
                    with st.expander(agent_name):
                        with st.chat_message("assistant", avatar = bot_image_2):
                            full_response = ""
                            message_placeholder = st.empty()
                            for chunk in response.split("\n"):
                                time.sleep(0.05)
                                message_placeholder.markdown(full_response + "▌")
                                full_response += chunk + "  \n" 
                                message_placeholder.markdown(full_response)
                else:
                    with st.chat_message("assistant", avatar = bot_image_2):
                        full_response = ""
                        message_placeholder = st.empty()
                        for chunk in response.split("\n"):
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "▌")
                            full_response += chunk + "  \n" 
                            message_placeholder.markdown(full_response)
                
                current_time = str(datetime.datetime.now())
                st.session_state.turn_id = current_time
                
                st.session_state.messages.append({"role": "assistant", "content": response, "chat_id": st.session_state.chat_id, "turn_id":  st.session_state.turn_id,
                                                "raw_content": "",
                                                "agent_name": agent_name,
                                                })
                st.session_state.context.append({"role": "system", "content": ""})

                if Is_Human_Required == True or response == "":
                    break
                else:
                    prompt = " "

            csv_file = f"data/{st.session_state.username}.csv"
            file_exists = os.path.isfile(csv_file)
            if not file_exists:
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['username','chat_id','turn_id','user_text','generative_text','raw_input','raw_output','engine','frontend_query_time','backend_query_time','history'])
            with open(csv_file, mode='a', newline='', encoding = 'utf-8') as file:
                writer = csv.writer(file)
                current_time = str(datetime.datetime.now())
                st.session_state.turn_id = current_time
                writer.writerow([st.session_state.username, st.session_state.chat_id, st.session_state.turn_id, prompt, full_response, "", "", context_radio, frontend_query_time, "", response_dict['history']])
            st.rerun()

elif st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect. If you encounter any issues related to user login, please contact Thanatchon Chongmankhong at thanatcc@bot.or.th.")
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password. If you encounter any issues related to user login, please contact Thanatchon Chongmankhong at thanatcc@bot.or.th.')