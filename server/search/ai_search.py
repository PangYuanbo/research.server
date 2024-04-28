import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def ai_research(need: str, researches: str):
    messages = [
        {"role": "user", "content": need},
        {"role": "system", "content": researches},
        {"role": "system",
         "content": "根据 user 的 need 匹配相关的 researches 并传出 researches 对应的所有字段，和原来的格式一致，给我一系列匹配的数据，字段要求是 [{title: '标题', description: '描述', money:'酬劳', location: '位置', univercity: '大学', isFullTime:'是否全职'}]，然后将这个数组传出，如果没有数据那么你就返回你觉得相关的，无论如何都要返回至少两条数据，你不要说任何其他的废话，只需要返回数据，你返回的形式和上面说的格式一致"}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response.choices[0].message.content
