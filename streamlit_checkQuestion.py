import streamlit as st
from PIL import Image
import base64
from openai import OpenAI

# OpenAI APIキーの設定（Streamlit Secretsから）
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit画面設定
st.set_page_config(page_title="歯科医師国家試験・問題校正", layout="centered")
st.title("🦷 歯科医師国家試験｜問題画像から校正チェック（GPT-4o VISION）")

# アップロード欄
uploaded_file = st.file_uploader("📄 歯科医師国家試験の問題画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    with st.spinner("🔍 GPT-4o Visionで解析・校正中..."):

        # base64形式にエンコード
        image_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode()

        # OpenAI Vision APIへのリクエスト
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは歯科医師国家試験問題の校正者です。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """この画像には複数の歯科医師国家試験問題が含まれています。
それぞれの問題について、以下の4点を実行してください。

1. 問題文が医学的・論理的に妥当かどうかをチェックしてください。
2. 誤字脱字や選択肢の形式ミスがないかを確認し、修正案があれば出してください。
3. 国家試験問題として適切な形式か（設問構造・選択肢の体裁）を評価してください。
4. 画像の中の問題はかなりの確率で間違っているので、記述されている正解答を正しいとは忖度しないで。回答は無視してGPTが回答を出して。一致したらOK違ったら、必ず報告して。
各問題ごとに見やすく整理して出力してください。"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=4096
        )

        # 結果出力
        result = response.choices[0].message.content

    st.subheader("📘 校正結果")
    st.markdown(result)
