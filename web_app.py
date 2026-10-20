import streamlit as st
from app import get_ai_response, load_document, split_into_chunks
import json  # Read and write chat history in JSON format
import uuid  # Generate a unique ID for each conversation


# Load document and prepare chunks
document_text = load_document()
chunks = split_into_chunks(document_text)




# Load saved chat history from the JSON file
def load_chat_history():
    try:
        # Open the history file in read mode
        with open("chat_history.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # Return an empty list if the file does not exist
        return []



# Load all saved conversations from the JSON file
def load_chats():
    try:
        # Open the conversations file in read mode
        with open("chats.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # Return an empty dictionary if the file does not exist
        return {}


# Save all conversations to the JSON file
def save_chats(chats):
    # Open the conversations file in write mode
    with open("chats.json", "w", encoding="utf-8") as file:
        json.dump(chats, file, indent=4, ensure_ascii=False)



# Page title
st.title("Local AI Chatbot")
st.caption("Your personal AI assistant powered by Ollama")



# Load saved conversations
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

# Track the currently selected conversation
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# Create the sidebar
with st.sidebar:
# Display the sidebar heading
    st.title("💬 Your Chats")
    # Create a new conversation
    if st.button("＋ New Chat", key="new_chat_button", use_container_width=True):
        chat_id = str(uuid.uuid4())
        st.session_state.chats[chat_id] = {
            "title": "New Chat",
            "messages": []
        }
        st.session_state.current_chat_id = chat_id
        save_chats(st.session_state.chats)
        st.rerun()

    
    # Display saved conversations with an options menu
    for chat_id, chat in list(st.session_state.chats.items()):
        col1, col2 = st.columns([5, 1])

        
        # Open the selected conversation
        with col1:
            is_active = st.session_state.current_chat_id == chat_id

            if st.button(
                f"{'🔵 ' if is_active else ''}{chat['title']}",
                key=f"open_{chat_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_chat_id = chat_id
                st.rerun()


        # Show conversation actions
        with col2:
            with st.popover("⋯"):
                
                # Rename the selected conversation
                with st.popover("Rename chat"):
                    new_title = st.text_input(
                        "Conversation name",
                        value=chat["title"],
                        key=f"rename_input_{chat_id}"
                    )

                    if st.button("Save name", key=f"rename_{chat_id}"):
                        cleaned_title = new_title.strip()

                        if cleaned_title:
                            st.session_state.chats[chat_id]["title"] = cleaned_title
                            save_chats(st.session_state.chats)
                            st.rerun()

                # Clear messages in this conversation
                if st.button("Clear chat", key=f"clear_{chat_id}"):
                    st.session_state.chats[chat_id]["messages"] = []

                    if st.session_state.current_chat_id == chat_id:
                        st.session_state.messages = []

                    save_chats(st.session_state.chats)
                    st.rerun()

                # Delete this conversation permanently
                if st.button("Delete chat", key=f"delete_{chat_id}"):
                    del st.session_state.chats[chat_id]

                    if st.session_state.current_chat_id == chat_id:
                        st.session_state.current_chat_id = None
                        st.session_state.messages = []

                    save_chats(st.session_state.chats)
                    st.rerun()




    
   


# Initialize the current conversation
if st.session_state.current_chat_id is None:
    st.session_state.messages = []
else:
    st.session_state.messages = st.session_state.chats[
        st.session_state.current_chat_id
    ]["messages"]



# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get user input and generate AI response
if prompt := st.chat_input("Message your AI assistant..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(
                st.session_state.messages, chunks
            )

        st.write(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

   
    # Save messages to the selected conversation
    if st.session_state.current_chat_id is not None:
        st.session_state.chats[
            st.session_state.current_chat_id
        ]["messages"] = st.session_state.messages

        # Set the conversation title from the first user message
        if st.session_state.chats[
            st.session_state.current_chat_id
        ]["title"] == "New Chat":
            st.session_state.chats[
                st.session_state.current_chat_id
            ]["title"] = prompt[:35]

        # Persist all conversations
        save_chats(st.session_state.chats)

