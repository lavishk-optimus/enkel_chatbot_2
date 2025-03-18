import streamlit as st
import time
import requests
# from auth import ret_func

# API_URL = "http://127.0.0.1:8000/api/chatbot/query"
# GET_URL = "http://127.0.0.1:8000/"

API_URL = "http://127.0.0.1:8000/api/chatbot/query"
GET_URL = "http://127.0.0.1:8000/"

# Function to fetch chat history
def fetch_chat_history(user_id):
    """Fetches chat history from a database (API call)."""
    try:
        history_response = requests.get(f"{GET_URL}/history/{user_id}")
        history = history_response.json().get("history", [])
        
        # Convert history to expected format
        formatted_history = []
        for msg in history:
            formatted_history.append({"role": "user", "content": msg["question"]})
            formatted_history.append({"role": "assistant", "content": msg["response"]})
        
        return formatted_history
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

# Function to save messages to DB
def save_message_to_db(user_id, role, content):
    """Simulated function to save chat to a database."""
    print(f"Saving to DB: {role} - {content}")




col1, col2, col3=st.columns([8,1,1])
with col3:
    if st.button("login"):
        st.write("login")
        # info=ret_func()
        # if info:
        #     st.write("logged in")
        # else:
        #     st.write("working")






# Simulated User Login
USER_ID = "1"  # Assume logged-in user

# # Initialize session state for messages
# if "messages" not in st.session_state:
#     st.session_state.messages = fetch_chat_history(USER_ID)  # Load chat history once

# # Display chat history from session state
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):  # Correct role usage
#         st.markdown(msg["content"])


def fetch_chat_history_fake():
    formatted_history = []
    
    formatted_history.append({"role": "user", "content": "user_ques history fake"})
    formatted_history.append({"role": "assistant", "content": "assistant anser history fake"})
        
    return formatted_history

if "messages" not in st.session_state:
    st.session_state.messages = fetch_chat_history_fake()  # Load chat history once




# Accept user input
user_input = st.chat_input("Ask me something...")
if user_input:
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
 
    # Placeholder for bot response (prevents duplicate fading issue)
    bot_placeholder = st.chat_message("assistant")
    response_placeholder = bot_placeholder.empty()  # Create an empty container

    with bot_placeholder:
        with st.spinner("Thinking..."):
            time.sleep(1)  # Simulate delay
            try:
                response = requests.post(API_URL, json={"question": user_input})
                print(response)
                bot_reply = response.json()
            except Exception as e:
                print(e)
                bot_reply=e
            

            # if response.status_code == 200:
            #     try:
            #         bot_reply = response.json().get("bot_response", "I'm sorry, I couldn't understand that.")
            #     except requests.exceptions.JSONDecodeError:
            #         bot_reply = "Error: Received invalid response from server."
            # else:
            #     bot_reply = f"Error: Server returned status code {response.status_code}"

        response_placeholder.markdown(bot_reply)  # Update the placeholder with the response

    # Append AI response to session state **after response is received**
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    print(bot_reply)

    # Save messages to database
    # save_message_to_db(USER_ID, "user", user_input)
    # save_message_to_db(USER_ID, "assistant", bot_reply)