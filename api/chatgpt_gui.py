from tkinter import *
from tkinter import ttk

import os
from openai import OpenAI


# APIキーの設定
api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=api_key)


# APIをコールする
def callOpenApi(content):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )

    result = completion.choices[0].message.content
    # print(result)
    return result


# テキストボックスに入力された質問を投げる
def throwQuestion():
    content = text.get()
    print("文字数：",len(content))
    if len(content) == 0:
        print("何か質問を入れてください")
        return
    print(content, "を質問します")
    response = callOpenApi(content)
    print(response)
    

# メインウィンドウ
root = Tk()
root.title("windowですよ")

# ラベル
qLabel = ttk.Label(root, text="プログラミングに関する質問を入力してください")

# テキストボックス
text = StringVar()
textBox = ttk.Entry(root, textvariable=text)

# ボタン
btn = ttk.Button(root, text="質問する", command=lambda:throwQuestion())

# 
qLabel.pack()
textBox.pack()
btn.pack()

##ウィンドウの表示
root.mainloop()