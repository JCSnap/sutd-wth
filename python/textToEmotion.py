import os
import openai
import constant

openai.organization = "org-bvlKBmngxqAVQHzFfuyAjggS"
openai.api_key = os.getenv("OPENAI_API_KEY")

def textToEmotion(text):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": constant.SYSTEM_MESSAGE},
        {"role": "user", "content": text}
    ]
    )

    emotion = completion.choices[0].message.content
    print(emotion)
    return emotion


textToEmotion("Hello, how are you?")
openai.Model.list()