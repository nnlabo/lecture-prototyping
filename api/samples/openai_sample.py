import os
from openai import OpenAI


api_key = os.getenv("OPEN_API_KEY")
# api_key = ""
client = OpenAI(api_key=api_key)


def call_open_ai(content):
    if not content:
        return "nothing"
    
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

if __name__ == "__main__":
    import sys
    content = "生成AIについて100文字以内で教えてください"
    if len(sys.argv) > 1:
        content = sys.argv[1]

    result = call_open_ai(content)
    print(result)