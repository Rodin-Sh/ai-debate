from openai import OpenAI
import streamlit as st

class Agent():
    def __init__(self, api_key, model, role, image, prompt, all_messages):
        self.api_key = api_key
        self.model = model
        self.role = role
        self.image = image

        self.client = OpenAI()
        all_messages.append({"role": self.role, "content": prompt})

    def generate_response(self, all_messages) -> str:
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=all_messages)
            
        all_messages.append({"role": self.role, "content": response.choices[0].message.content})
        st.session_state.messages.append({"role": self.image, "content": response.choices[0].message.content})

        return response.choices[0].message.content