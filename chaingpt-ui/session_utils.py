import openai
from streamlit import session_state as st_session


def init_session_state():
    if 'generated' not in st_session:
        st_session['generated'] = []
    if 'past' not in st_session:
        st_session['past'] = []
    if 'messages' not in st_session:
        st_session['messages'] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    if 'model_name' not in st_session:
        st_session['model_name'] = []
    if 'cost' not in st_session:
        st_session['cost'] = []
    if 'total_tokens' not in st_session:
        st_session['total_tokens'] = []
    if 'total_cost' not in st_session:
        st_session['total_cost'] = 0.0

def reset_session_state():
    st_session['generated'] = []
    st_session['past'] = []
    st_session['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st_session['number_tokens'] = []
    st_session['model_name'] = []
    st_session['cost'] = []
    st_session['total_cost'] = 0.0
    st_session['total_tokens'] = []

def generate_response(model, prompt):
    st_session['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st_session['messages']
    )
    response = completion.choices[0].message.content
    st_session['messages'].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens
