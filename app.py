import os
import time
from openai import OpenAI
import streamlit as st
import streamlit as st

# 비밀번호 설정
password = st.text_input("비밀번호를 입력하세요", type="password")
if password != st.secrets["APP_PASSWORD"]:
    st.stop()

# 비밀번호 맞으면 입력창 숨기기
st.empty()

# 로그인 시간 기록
if "login_time" not in st.session_state:
    st.session_state.login_time = time.time()

# 30분 지나면 로그아웃
if time.time() - st.session_state.login_time > 1800:
    st.session_state.clear()
    st.warning("세션이 만료됐어요. 다시 로그인해주세요.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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