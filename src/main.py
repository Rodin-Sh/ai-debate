from openai import OpenAI
from dotenv import load_dotenv
import os
import yaml
import time
import streamlit as st

from agents import Agent

def load_agent_prompts() -> dict:
    current_directory = os.path.dirname(__file__)
    filepath = os.path.join(current_directory, "./config/agents.yaml")
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

def get_agent_prompt(config: str, category: str, topic) -> str:
    prompt = config['agents'][category]['prompt']
    return prompt.format(topic=topic)

def main():
    
    # Initialization of all variables
    load_dotenv()
    # api_key = os.getenv("API_KEY")
    llm_model = "gpt-4o-mini"
    config = load_agent_prompts()
    all_messages = []

    # Set's the title of the web page on the tab navigation bar
    st.set_page_config(page_title='AI Debate')

    topic = ""
    st.title("AI Debate")
    
    with st.sidebar:
        api_key = st.text_input(label="OpenAI API Key", type="password")
        while api_key=="":
            st.write("Waiting on a topic...")
            st.stop()

        llm_model = st.selectbox("OpenAI Model",
        ('gpt-4o-mini', 'gpt-4o', 'gpt-4-turbo'))

        topic = st.text_input(label="Debate Topic", placeholder="God's existence")
        while topic == "":
            st.write("Waiting on a topic...")
            st.stop()

    st.caption(f'''About "{topic.strip().title()}"''')

    # Loads the believer and disagreer prompt from the agents.yaml file
    believer_prompt = get_agent_prompt(config, "believer", topic)
    disagreer_prompt = get_agent_prompt(config, "disagreer", topic)

    # Initialized variables used to set the colour of icon for streamlit
    believer_image = "assistant"
    disagreer_image = "user"

    # Creating instances of Agent() class
    believer = Agent(api_key, llm_model, "assistant", believer_image, believer_prompt, all_messages)
    disagreer = Agent(api_key, llm_model, "assistant", disagreer_image, disagreer_prompt, all_messages)

    # Copying all messages from all_messages to st.session_state.messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        for i in range(len(all_messages)):
            st.session_state.messages.append(
                {
                    "role": believer_image if i%2 == 0 else disagreer_image,
                    "content": all_messages[i]["content"]
                })

    
    # Starting from 3rd message because the first two are internal prompts for the agents
    for i in range(len(st.session_state["messages"][2:])):
        st.chat_message(believer_image if i%2 == 0 else disagreer_image).write(st.session_state.messages[i]["content"])

    for i in range(5):

        # The believer replies first
        reply_believer = believer.generate_response(all_messages)
        st.chat_message(believer_image).write(reply_believer)

        # Wait 5 seconds
        time.sleep(5)

        # The disagreer replies afterwards
        reply_disagreer = believer.generate_response(all_messages)
        st.chat_message(disagreer_image).write(reply_disagreer)

        # Wait 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    main()