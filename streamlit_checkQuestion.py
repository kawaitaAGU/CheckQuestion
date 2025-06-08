import streamlit as st
from PIL import Image
from openai import OpenAI

# OpenAIクライアント設定（secretsから取得）
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="歯科国試AI校正アプリ", layout="centered")
st.title("🦷 歯科医師国家試験｜画像から問題文校正（GPT-4o VISION）")

uploaded_file = st.file_uploader("画像ファイルをアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた問題画像", use_column_width=True)

    with st.spinner("GPT-4o Visionで解析中..."):

        # GPT-4o Visionへのクエリ
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは歯科医師国家試験問題の校正を行うAIです。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """以下の画像には、歯科医師国家試験の問題が複数含まれています。
それぞれの問題に対して：
1. 問題文が医学的・論理的に妥当かどうかを判定してください。
2. 誤字・脱字・選択肢の表記ミスなど、単純な校正ポイントがあれば指摘してください。
3. 形式が国家試験問題として成立しているかも含めて、必要に応じて修正例も示してください。
出力は見やすく問題ごとに整理してください。"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/jpeg;base64," + base64.b64encode(uploaded_file.getvalue()).decode()
                            }
                        }
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=4096
        )

        result = response.choices[0].message.content

    st.subheader("📘 校正結果とフィードバック")
    st.markdown(result)