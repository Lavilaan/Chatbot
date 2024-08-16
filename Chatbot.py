import streamlit as st
from streamlit_chat import message
from langchain_community.llms import Ollama

# Setting page title and header
st.set_page_config(page_title="Task Code Generator", layout="wide")
st.markdown("<h1 style='text-align: center;'>Task Code Generator</h1>", unsafe_allow_html=True)

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = "llama3:latest"

# Sidebar - let user choose model and set temperature
with st.sidebar:
    st.header("Settings")
    st.session_state['model_name'] = st.selectbox("Select Model", ["llama3:latest", "phi3:latest"])
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=1.0)

# Function to initialize the selected model
def get_model(model_name):
    return Ollama(
        base_url='http://localhost:11434',
        model=model_name
    )

# Function to generate responses
def generate_response(system_instructions, user_prompt, model_name):
    ollama = get_model(model_name)
    
    prompt_template = f"""
    {system_instructions}
    
    Task Description:
    {user_prompt}
    """
    response = ollama.invoke(prompt_template)
    return response

# Container for chat history
response_container = st.container()
# Container for text input
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        system_instructions = st.text_area("Enter system instructions")
        user_input = st.text_area("Describe the task:")
        submit_button = st.form_submit_button(label='Send')

    if submit_button and system_instructions and user_input:
        output = generate_response(system_instructions, user_input, st.session_state['model_name'])
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
