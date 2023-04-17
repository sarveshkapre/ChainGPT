import openai
import streamlit as st
from streamlit_chat import message


from session_utils import init_session_state, reset_session_state, generate_response
from settings import OPENAI_API_KEY

# Setting page title and header
st.set_page_config(page_title="GPT-X", page_icon=":bulb:", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>GPT-X</h1>", unsafe_allow_html=True)

# Set API key
openai.api_key = OPENAI_API_KEY

# Initialise session state variables
init_session_state()

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Settings")
st.sidebar.markdown("Welcome to GPT-X! This AI-powered chatbot uses OpenAI's GPT-based language models to generate human-like responses.")
st.sidebar.markdown("Select a model to use in the conversation below:")
model_name = st.sidebar.radio("", ("GPT-3.5", "GPT-4"))
st.sidebar.markdown("Provide a document link to use in the conversation:")
url = st.sidebar.text_input("Document URL:")
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    reset_session_state()
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

# Improve UI with padding and separators
st.markdown("<style>body {margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529; text-align: left; background-color: #000000;}</style>", unsafe_allow_html=True)
st.markdown("<style>h1{color:#ffffff;}</style>", unsafe_allow_html=True)
st.markdown("<style>.container{padding: 1rem;}</style>", unsafe_allow_html=True)
st.markdown("<style>hr{border-color: #6c757d;}</style>", unsafe_allow_html=True)

response_container = st.container()
st.write("---")
container = st.container()


with container:
    with st.form(key='my_form', clear_on_submit=True):
        st.markdown("Enter your message")
        user_input = st.text_area("", key='input', height=75)
        submit_button = st.form_submit_button(label='Send', help="Press 'Enter' to submit or 'Shift+Enter' to add a new line.")

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(model, user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
