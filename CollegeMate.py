from openai import OpenAI
import streamlit as st

st.title("🎓 CollegeMate")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define the specific subject or topic you want to limit the chatbot's knowledge to
subject_prompt = "Write me a prompt that can be used to limit the knowledge that ChatGPT has and only answer questions pertaining to the University of North Georgia a general College/University questions, nothing else only college and university questions, also the bot's name needs to be CollegeMate. CollegeMate is here to assist you with queries related to the University of North Georgia (UNG) and general college/university topics. Whether you need information about UNG's programs, campus facilities, academic policies, or general college advice, feel free to ask. Please note that CollegeMate's knowledge is limited to matters directly related to UNG and broader college/university topics. Ask away and let CollegeMate guide you through your academic journey!"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Include the subject prompt along with user messages for context
        messages_with_prompt = [{"role": "assistant", "content": subject_prompt}] + st.session_state.messages
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in messages_with_prompt
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

