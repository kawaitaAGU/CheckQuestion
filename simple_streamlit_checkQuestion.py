import streamlit as st
from PIL import Image
import base64
from openai import OpenAI

# OpenAI APIキーの設定（Streamlit Secretsから）
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit画面設定
st.set_page_config(page_title="問題校正", layout="centered")
st.title("🦷 Simple問題画像から校正チェック（GPT-4o VISION）")

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
                            "text": """この画像には、歯科医師国家試験の形式に準じた問題・選択肢・正解・解説が含まれています。

正答は「解答：」「正解：」などのあとに明示されますが、それが「問題番号」ではなく「正しい選択肢番号」を示していることを理解し、正確に読み取ってください（例：「解答：14」は選択肢番号1と4の意味）。他の数字に惑わされないよう注意してください。

以下の点をチェックし、各問題ごとに簡潔に整理して出力してください：

1. 問題文と選択肢が論理的・医学的に妥当か。
2. 各選択肢が正しいか誤っているかを評価。
3. 「○つ選べ」の指示と正解数が整合しているか。
4. 画像内の正答とあなたの答えが一致するか（異なる場合は理由を述べて報告）。
5. 専門用語や表記に誤字・脱字・用語ミスがないか。
6. 国家試験問題としての形式（選択肢の体裁や設問構造）が適切か。
7. 解説がある場合、その内容が妥当か。

※ 問題内の正答は間違っていることもあるため、忖度せず厳密に判断してください。"""
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
