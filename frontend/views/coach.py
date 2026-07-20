import streamlit as st
import requests
from frontend.services import api_client

def render() -> None:
    st.title("💬 AI Resume Coach")
    st.markdown(
        "Ask questions about how to format your CV, explain your experience, "
        "highlight technical skills, or tailor your profile to a job description."
    )

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("⚠️ Please sign in from the sidebar to chat with the AI Resume Coach.")
        st.info("The AI Coach uses your past resume analyses (if available) to give personalized feedback.")
        return

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Sidebar controls
    with st.sidebar:
        st.markdown("---")
        st.markdown("## 💬 Coach Controls")
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()

    # Display past messages
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Accept user input
    user_query = st.chat_input("Ask your question here...")

    if user_query:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_query)
        
        # Add user message to chat history
        st.session_state["chat_history"].append({"role": "user", "content": user_query})

        # Call backend API
        try:
            with st.spinner("Coach is thinking..."):
                result = api_client.send_chat_message(
                    message=user_query,
                    history=st.session_state["chat_history"][:-1],  # send history except current query
                    access_token=access_token
                )
                assistant_response = result.get("response", "I could not generate a response.")
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
                
            # Add assistant response to history
            st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
            st.rerun()
            
        except requests.RequestException as exc:
            st.error("Could not reach the coach API. Please ensure the backend is running.")
            if exc.response is not None:
                st.caption(f"Details: {exc.response.text}")
