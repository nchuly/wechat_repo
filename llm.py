from openai import OpenAI
import json
import random

API_SECRET_KEY = "sk-zk2eff0d826eb0ecb95c96e1dcc6b2c27c467e2592735773"
BASE_URL = "https://api.zhizengzeng.com/v1/"

def chat_completions4(query):
    client = OpenAI(api_key=API_SECRET_KEY, base_url=BASE_URL)
    resp = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    # print(resp)
    print(resp.choices[0].message.content)
    return resp.choices[0].message.content

def query_llm(week='星期一', max_temp=20, min_temp=10, weather="多云" ):
    song_prompt = "给我推荐二十句焦安溥和张悬的歌的歌词，歌词长度不要超过十八个字，要求歌词有意义，不要只是随便的一句歌词。以json的形式输出，如{歌曲名称：推荐歌词}，不要有额外的回答"
    care_prompt = f"以一个男朋友的口吻对一个女生说一句关心的话，今天是{week},今天的天气是{weather}, 今天最高气温是{max_temp}, 最低气温是{min_temp},说的这句话不需要太长，十五个字以内，以json的形式输出，key就是<care>，value就是你要说的话，注意字数限制"
    song_value = "我出错了呜呜呜"
    care_value = "我出错了呜呜呜"

    for i in range(0, 10):
        try:
            resp = chat_completions4(song_prompt).strip().strip('```json').strip('```')
            resp = json.loads(resp)
            random_key = random.choice(list(resp.keys()))
            song_value = f"{resp[random_key]}"
            break
        except json.JSONDecodeError as e:
            print("字符串格式错误:", e)

    for i in range(0, 10):
        try:
            resp = chat_completions4(care_prompt).strip().strip('```json').strip('```')
            resp = json.loads(resp)
            random_key = random.choice(list(resp.keys()))
            care_value = f"{resp[random_key]}"
            break
        except json.JSONDecodeError as e:
            print("字符串格式错误:", e)

    return care_value, song_value

if __name__ == '__main__':
    re = query_llm()
    print(re)