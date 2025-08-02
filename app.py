from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

# Webアプリの概要・操作方法
st.title("スポーツ医療専門家 LLMアプリ")
st.markdown("""
このWebアプリは、スポーツ医療の専門家として振る舞うLLM（大規模言語モデル）に質問できるサービスです。  
操作方法：  
1. 下のラジオボタンで専門家の種類を選択してください。  
2. 質問内容を入力フォームに記入し、「送信」ボタンを押してください。  
3. LLMによる回答が画面に表示されます。
""")

# 専門家の種類（ラジオボタン）
expert_type = st.radio(
    "専門家の種類を選択してください：",
    ("一般的な専門家", "スポーツ医療の専門家")
)

# 入力フォーム
user_input = st.text_area("質問内容を入力してください：")

# LLMから回答を取得する関数
def get_llm_response(input_text: str, expert: str) -> str:
    # システムメッセージを選択値に応じて変更
    if expert == "スポーツ医療の専門家":
        system_prompt = "あなたはスポーツ医療の専門家です。医学的知識とスポーツ現場での経験を活かして、質問者に分かりやすく丁寧に回答してください。"
    else:
        system_prompt = "あなたは一般的な専門家です。質問者に分かりやすく丁寧に回答してください。"

    # OpenAI APIキーの取得
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.2, model_name="gpt-3.5-turbo")

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]
    response = chat.invoke(messages)
    return response.content

# 送信ボタン
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問内容を入力してください。")
    else:
        with st.spinner("LLMが回答中..."):
            answer = get_llm_response(user_input, expert_type)
        st.markdown("#### 回答")
        st.write(answer)
