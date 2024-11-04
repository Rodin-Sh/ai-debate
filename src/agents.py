from openai import OpenAI
import streamlit as st

class Agent():
    def __init__(self, api_key, model, role, image, prompt, all_messages):
        self.api_key = api_key
        self.model = model
        self.role = role
        self.image = image

        # Initializing the OpenAI client using api_key
        self.client = OpenAI()

        # Adding the first message on initialization, which is the agent prompt
        all_messages.append({"role": self.role, "content": prompt})

    def generate_response(self, all_messages) -> str:
        
        # Generating a response from OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=all_messages)
            
        # Adding that response to both agents
        all_messages.append({"role": self.role, "content": response.choices[0].message.content})

        # Slightly dfferent for streamlit because we are using "assistants" roles
        # To get the different coloured icons from Streamlit, we need to set one to "user"
        # and the other one to "assistant"
        st.session_state.messages.append({"role": self.image, "content": response.choices[0].message.content})

        # Returning message
        return response.choices[0].message.content