import streamlit as st
from langGrapgh_backend import chatbot
from langchain_core.messages import HumanMessage
#st.session State => dict -> save even referh page

# message_history = []

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
#loading the hisrty conversation
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

thread_id = '1'
CONFIG = {'configurable':{"thread_id":thread_id}}



user_input = st.chat_input("Type Here....")
# fist add message in messsage hostory
if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in  chatbot.stream(
            {'messages':[HumanMessage(content=user_input)]},
            config={'configurable':{"thread_id":'thread 01'}},
            stream_mode="messages"

            )
        )

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})