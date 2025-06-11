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
                            "text": """この画像には、歯科医師国家試験の形式に準じた問題・選択肢・正答・解説が含まれています。

あなたは、これらの問題について校正・評価を行う専門の校正者です。

正答は通常「解答：」「正解：」などのあとに記載されていますが、それは問題番号ではなく「正しい選択肢の番号」を示していることを理解してください。
例：「解答：14」は選択肢1番と4番が正解であることを意味します。他の数字（問題番号や注記番号）と混同しないよう注意してください。

---

以下の点について、各問題ごとに明確に整理して評価・出力してください：

1. 問題文の意味が論理的・医学的に妥当であるか。
2. 各選択肢が正しいか誤っているか、根拠を添えて判断すること。

3. 各選択肢の正誤を、問題文の選択数指示とは**完全に無関係に**、独立して厳密に判定してください。  
そのうえで、問題文に記された「◯つ選べ」という指示と、あなたが判断した「正しい選択肢の数」が一致しているかを必ず比較してください。

- 一致しない場合（例：「2つ選べ」とあるが実際には3つ正しい）には、**その矛盾を明確に指摘し、「問題の構造に誤りがある」または「正答の表示に誤りがある」と報告してください。**
- 決して問題の形式にあわせて正解を“無理に2つに抑え込まない”でください。
- 必ず、「あなたが正しいと判断した選択肢番号」をすべて列挙し、その数と設問の指示数が一致するかを照合してください。

4. GPTが判断した正解と、画像内の正解表示（解答：など）が一致しているかを確認してください。  
   一致しない場合はその理由を明示し、「問題の正答表示に誤りがある」と報告してください。

5. 専門用語・表現に誤字・脱字・表記ミスがないかを確認してください。
6. 国家試験問題としての構成（選択肢の体裁、設問構造、選択肢の数など）が適切であるか簡潔に評価してください。
7. 解説がある場合は、その記述内容が医学的に妥当かどうかをチェックして簡潔に報告してください。

※ 問題ごとに見やすく出力してください。表現は簡潔・明確に。  
※ 解答に忖度せず、あなた自身の判断をもとに厳密な評価を行ってください。
"""
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
