"""
Chat Manager

Handles:
- Chat history
- User messages
- AI messages (with reasoning details & sources)
- Clear chat
- Export conversation
"""

import streamlit as st


class ChatManager:

    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []

    # ------------------------------------
    # Add User Message
    # ------------------------------------

    def add_user_message(self, message):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

    # ------------------------------------
    # Add Assistant Message
    # ------------------------------------

    def add_ai_message(self, message, reasoning_details=None, sources=None):
        msg_obj = {
            "role": "assistant",
            "content": message
        }
        if reasoning_details:
            msg_obj["reasoning_details"] = reasoning_details
        if sources:
            msg_obj["sources"] = sources

        st.session_state.messages.append(msg_obj)

    # ------------------------------------
    # Display Chat
    # ------------------------------------

    def display_chat(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Render reasoning steps if available for AI assistant
                if message.get("role") == "assistant" and message.get("reasoning_details"):
                    with st.expander("🧠 Model Internal Reasoning Steps"):
                        reasoning = message["reasoning_details"]
                        if isinstance(reasoning, (dict, list)):
                            st.json(reasoning)
                        else:
                            st.markdown(str(reasoning))

                st.markdown(message["content"])

    # ------------------------------------
    # Clear Chat
    # ------------------------------------

    def clear_chat(self):
        st.session_state.messages = []

    # ------------------------------------
    # Export Chat
    # ------------------------------------

    def export_chat(self):
        conversation = ""
        for message in st.session_state.messages:
            role = message["role"].capitalize()
            conversation += f"{role}\n"
            conversation += "-" * 20 + "\n"
            if message.get("reasoning_details"):
                conversation += f"[Reasoning Details: {message['reasoning_details']}]\n\n"
            conversation += message["content"]
            conversation += "\n\n"
        return conversation

    # ------------------------------------
    # Total Messages
    # ------------------------------------

    def total_messages(self):
        return len(st.session_state.messages)