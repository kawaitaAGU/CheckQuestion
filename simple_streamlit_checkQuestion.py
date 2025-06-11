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
                            それぞれの問題について、以下の点をチェックしてください。
問題文と選択肢と正解答と解説で校正されています。
選択肢は通常は５個ですが、それ以上の場合もあります。
場合によっては問題の説明が附属している場合もあります。
その場合、問題を説明する説明文として妥当か結果だけ報告してください。
まず問題文に対して各選択肢が正しいかどうかチェックしてください。
選択肢の内容が正しいかどうかはひとつひとつ厳密にチェックしなさい。
1つ選べ、２つ選べ、３つ選べなど選択指示の数と正しい記述の選択肢の数が間違っている時も回答がおかしいと明確に指摘してください。
回答の妥当性については辛めの評価をしてください。正解答に関してはきわめて厳密な校正をしてください。
1. 問題文が医学的・論理的に妥当かどうかをチェックしてください。評価結果は結果だけシンプルに返してください。
2. 誤字脱字や選択肢の形式ミスがないかを確認し、修正案があれば出してください。ミスが検出された時ははっきりと報告しなさい。
3. 国家試験問題として適切な形式か（設問構造・選択肢の体裁）を評価してください。評価結果はごくシンプルに返してください。
4. 画像の中の問題はかなりの確率で間違っているので、記述されている正解答を正しいとは忖度しないで。回答は無視してGPTが回答を出して。
一致したらOK。違ったら、必ず報告してください。

各問題ごとに見やすく整理して出力してください。報告全体は把握しやすいようにシンプルにしてください。"""
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
