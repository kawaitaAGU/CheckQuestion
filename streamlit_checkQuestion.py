import streamlit as st
from PIL import Image
import base64
from openai import OpenAI

# OpenAIクライアント設定（secretsから取得）
# OpenAI APIキーの設定（Streamlit Secretsから）
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="歯科国試AI校正アプリ", layout="centered")
st.title("🦷 歯科医師国家試験｜画像から問題文校正（GPT-4o VISION）")
# Streamlit画面設定
st.set_page_config(page_title="歯科医師国家試験・問題校正", layout="centered")
st.title("🦷 歯科医師国家試験｜問題画像から校正チェック（GPT-4o VISION）")

uploaded_file = st.file_uploader("画像ファイルをアップロードしてください", type=["png", "jpg", "jpeg"])
# アップロード欄
uploaded_file = st.file_uploader("📄 歯科医師国家試験の問題画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file:
image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた問題画像", use_column_width=True)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    with st.spinner("GPT-4o Visionで解析中..."):
    with st.spinner("🔍 GPT-4o Visionで解析・校正中..."):

        # GPT-4o Visionへのクエリ
        # base64形式にエンコード
        image_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode()

        # OpenAI Vision APIへのリクエスト
response = client.chat.completions.create(
model="gpt-4o-2024-11-20",
messages=[
{
"role": "system",
                    "content": "あなたは歯科医師国家試験問題の校正を行うAIです。"
                    "content": "あなたは歯科医師国家試験問題の校正者です。"
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
                            "text": """この画像には複数の歯科医師国家試験問題が含まれています。
それぞれの問題について、以下の3点を実行してください。

1. 問題文が医学的・論理的に妥当かどうかをチェックしてください。
2. 誤字脱字や選択肢の形式ミスがないかを確認し、修正案があれば出してください。
3. 国家試験問題として適切な形式か（設問構造・選択肢の体裁）を評価してください。

各問題ごとに見やすく整理して出力してください。"""
},
{
"type": "image_url",
"image_url": {
                                "url": "data:image/jpeg;base64," + base64.b64encode(uploaded_file.getvalue()).decode()
                                "url": f"data:image/jpeg;base64,{base64_image}"
}
}
]
@@ -49,7 +58,8 @@
max_tokens=4096
)

        # 結果出力
result = response.choices[0].message.content

    st.subheader("📘 校正結果とフィードバック")
    st.markdown(result)
    st.subheader("📘 校正結果")
    st.markdown(result)
