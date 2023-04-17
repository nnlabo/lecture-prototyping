from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

import os
from turtle import heading
import openai

# APIキーの設定
openai.api_key = os.getenv("OPEN_API_KEY")

# APIをコールする
def callOpenApi(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": content},
        ],
    )
    return response
    
# テキストボックスに入力された質問を投げる
def throwQuestion():
    content = text.get()
    print("文字数：",len(content))
    if len(content) == 0:
        print("何か質問を入れてください")
        return
    print(content, "を質問します")
    response = callOpenApi(content)
    print(response.choices[0]["message"]["content"].strip())
    

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