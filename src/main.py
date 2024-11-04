from openai import OpenAI
from dotenv import load_dotenv
import os
import yaml
import time

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
    api_key = os.getenv("API_KEY")
    llm_model = "gpt-4o-mini"
    config = load_agent_prompts()
    all_messages = []

    # topic = input("TOPIC:")
    topic = "God's existence"

    believer_prompt = get_agent_prompt(config, "believer", topic)
    disagreer_prompt = get_agent_prompt(config, "disagreer", topic)

    print(believer_prompt)
    print(disagreer_prompt)

    believer = Agent(api_key, llm_model, "assistant", believer_prompt, all_messages)
    disagreer = Agent(api_key, llm_model, "assistant", disagreer_prompt, all_messages)

    for i in range(3):
        reply_believer = believer.generate_response(all_messages)
        print(f"Believer: {reply_believer}")
        print("")
        
        time.sleep(3)

        reply_disagreer = disagreer.generate_response(all_messages)
        print(f"Disagreer: {reply_disagreer}")
        print("")

        time.sleep(3)

if __name__ == "__main__":
    main()