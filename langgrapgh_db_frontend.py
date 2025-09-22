import streamlit as st
from langgrapgh_db_backend import chatbot , retrive_all_thread
from langchain_core.messages import HumanMessage
import uuid
#st.session State => dict -> save even referh page

# message_history = []

# UTILS *********************************************
def thread_generation_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = thread_generation_id()
    st.session_state['thread_id'] = thread_id
    add_thread_ID(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread_ID(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_converation(thread_id):
    state = chatbot.get_state(config={'configurable':{"thread_id":thread_id}})
    return state.values.get('messages',[])
#** SESSION SETUP *************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = thread_generation_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_all_thread()


add_thread_ID(st.session_state['thread_id'])


# ************************ SIDEBAR UI *******************

st.sidebar.title('LangGraph ChatBot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header("My Conversation")

for thread_id in st.session_state['chat_threads'][::]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_converation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages

#loading the history conversation
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

CONFIG = {'configurable':{"thread_id":st.session_state['thread_id']}}



user_input = st.chat_input("Type Here....")
# fist add message in messsage history
if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in  chatbot.stream(
            {'messages':[HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages"

            )
        )

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})