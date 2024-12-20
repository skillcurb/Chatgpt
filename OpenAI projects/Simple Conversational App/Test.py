#import libraries
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import streamlit as st

import os

#set environment variable for openAI API key
os.environ["OPENAI_API_KEY"]="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"

#initialize the ChatOpenAI by providing temperature and model
chat = ChatOpenAI(temperature=.7, model='gpt-3.5-turbo')

#  *****Code for StreamLit UI from here down****

#set page configurations
st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
st.header("Hey, I'm your Chat GPT")

# Initialize session state and set a default system message
if "sessionMessages" not in st.session_state:
     st.session_state.sessionMessages = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# Define a function to get text input from the user
def get_text():
    input_text = st.text_input("You: ", key=input)
    return input_text


# Get user input and create a 'Generate' button
user_input = get_text()
submit = st.button('Generate Response')

# Define a function to load the answer to a question
def load_answer(question):

    # Add the user's question as a HumanMessage to the session messages
    st.session_state.sessionMessages.append(HumanMessage(content=question))

    # Get the assistant's answer using the chat model
    assistant_answer = chat(st.session_state.sessionMessages)

    # Add the assistant's answer as an AIMessage to the session messages
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))

    # Return the assistant's answer
    return assistant_answer.content

# If the 'Generate Response' button is clicked
if submit:
    # Load the answer for the user input and display it
    response = load_answer(user_input)
    st.subheader("Answer:")
    st.write(response, key=1)







