import streamlit as st
import requests
import json
st.title("AI chat application")
if "messages" not in st.session_state:
    st.session_state.messages=[]

for i in st.session_state.messages:
    if i["role"]=="user":

        with st.chat_message("user"):
            st.markdown(i["content"])
    else:
        with st.chat_message("ai"):
            st.markdown(i["content"])

uploaded_pdf = st.file_uploader("Attach a PDF", type="pdf")

if uploaded_pdf is not None:
    st.markdown("**PDF Uploaded**")
    user_msg=st.chat_input("ASk about the PDF")
else:
    user_msg=st.chat_input("Chat with AI")

if user_msg!=None and user_msg!="":
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("ai"):
        if uploaded_pdf==None:
            #this generates using gemini API based on question/user query
            ai_msg=requests.post("http://127.0.0.1:8000/api/",json={"question":user_msg,"chat": json.dumps(st.session_state.messages)})
            st.markdown(ai_msg.json()["text"])
        else:
            #this generates response from pdf
            files = {"pdf":uploaded_pdf}
            data = {"question": user_msg,"chat": json.dumps(st.session_state.messages)}
            ai_msg = requests.post("http://127.0.0.1:8000/rag/", files=files, data=data)
            st.markdown(ai_msg.json()["text"])

    st.session_state.messages.append({"role":"user","content":user_msg})
    st.session_state.messages.append({"role":"ai","content":ai_msg.json()["text"]})

   