import streamlit as st
from PIL import Image
import io
import base64
import os
from openai import OpenAI
import time

# OpenAI APIキーの読み込み (.streamlit/secrets.toml に保存済み)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="国家試験問題チェック", layout="wide")
st.title("歯科医師国家試験画像チェックアプリ")

uploaded_files = st.file_uploader("試験問題の画像を50枚までアップロードしてください", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for i, uploaded_file in enumerate(uploaded_files[:50]):
        st.markdown(f"### 📄 ファイル {i+1}: `{uploaded_file.name}` の解析結果")

        # 画像を表示
        image = Image.open(uploaded_file)
        st.image(image, caption=f"アップロード画像 {i+1}", use_column_width=True)

        # 画像をBase64に変換
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        # GPT-4oへ送信
        try:
            with st.spinner("GPTで解析中..."):
                response = client.chat.completions.create(
                    model="gpt-4o-2024-11-20",
                    messages=[
                        {
                            "role": "system",
                            "content": "あなたは歯科医師国家試験問題の専門家です。画像から読み取った国家試験の問題文・選択肢・正解を校正・評価してください。"
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "以下は試験問題画像です。問題文、選択肢、正答が問題として成立しているか、校正ミスがないか、正答が妥当かを確認し、全体の評価と解説を出力してください。"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.3,
                    max_tokens=1500
                )

                result = response.choices[0].message.content
                st.success("✅ 解析完了")
                st.markdown("#### 評価結果")
                st.markdown(result)

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
