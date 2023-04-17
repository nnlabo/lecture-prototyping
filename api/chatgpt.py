import os
import openai

# APIキーの設定
openai.api_key = os.getenv("OPEN_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "理系の高校生がやる気になる褒め言葉を教えてください"},
    ],
)
print(response.choices[0]["message"]["content"].strip())