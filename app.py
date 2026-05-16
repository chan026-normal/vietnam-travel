from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🇻🇳 A조 베트남 AI 여행 가이드")
st.caption("하노이, 호치민, 다낭 등 베트남 여행 정보를 물어보세요!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("예: 하노이 3박 4일 일정 짜줘"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 베트남 전문 여행 가이드입니다. 실용적인 여행 정보를 한국어로 안내해주세요."},
                    *st.session_state.messages
                ]
            )
            reply = response.choices[0].message.content
            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})