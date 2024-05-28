import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
import re
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def call_llm_with_messages(message):
    messages = [
        {"role": "system", "content": "assistant"},
        {"role": "user", "content": message},
    ]
    response = Generation.call(
        model="qwen-max",
        messages=messages,
        # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
        seed = random.randint(0, 1000),
        # 将输出设置为"message"格式
        result_format="message",
    )
    if response.status_code == HTTPStatus.OK:
        poluted_json = response.output.choices[0].message.content
        print(poluted_json)
        return poluted_json
    else:
        print(
            "Request id: %s, Status code: %s, error code: %s, error message: %s"
            % (
                response.request_id,
                response.status_code,
                response.code,
                response.message,
            )
        )


def purify_json(poluted_json):
    json_match = re.search(r"\{.*\}", poluted_json, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        # 去掉注释
        json_str = re.sub(r"//.*", "", json_str)
        try:
            # 尝试将字符串解析为JSON
            json_obj = json.loads(json_str)
            return json_obj
        except json.JSONDecodeError as e:
            print("Invalid JSON format:", e)
            return None
    else:
        print("No JSON found in text.")
        return None




def transform_json(original, desired):
    transformed = desired.copy()
    
    transformed['activity']['activity_id'] = original['activity'].get('activity_id', "")
    transformed['activity']['start_time'] = original['activity'].get('start_time', "")
    transformed['activity']['end_time'] = original['activity'].get('end_time', "")
    
    location = original['activity'].get('location', {})
    transformed['activity']['location']['address'] = location.get('address', "")
    transformed['activity']['location']['latitude'] = location.get('latitude', "")
    transformed['activity']['location']['longitude'] = location.get('longitude', "")
    
    transformed['activity']['participants'] = [
        {
            "name": p.get('name', ""),
            "qu_id": p.get('qu_id', ""),
            "tasks": p.get('tasks', [])
        } for p in original['activity'].get('participants', [])
    ]
    
    transformed['activity']['description'] = original['activity'].get('description', "")
    transformed['activity']['tags'] = original['activity'].get('tags', [])
    
    return transformed


if __name__ == "__main__":
    prompt_str = """
                请帮我根据后面一段对话填充如下json数据结构
                {
                    "activity": {
                        "activity_id": "",
                        "start_time": "",
                        "end_time": "",
                        "location": {
                        "address": "",
                        "latitude": 
                        "longitude": 
                        },
                        "participants": [
                        {
                            "name": "",
                            "qu_id": "",
                            "tasks": []
                        },
                        
                        ],
                        "description": "",
                        "tags": [
                        
                        ]
                    }
                }
                注意请仅仅返回json本身！不要返回其他任何字符！对于tag这一field，请根据对话内容生成合适的tag,tag请使用中文。
                如果对话中决定了某个人在活动中的任务，请在“description”中列出。请确保不要在JSON中增加任何新字段。
                对话：
                """
    conversation_content = """
                小明(qu_id:789): 小红，我们明天上午一起去公园野餐怎么样？
                小红(qu_id:101): 好啊！我们去人民公园吧，早上10点怎么样？
                小明(qu_id:789): 10点太早了，11点可以吗？我们在哪里见面？
                小红(qu_id:101): 好的，11点在人民公园南门见面吧
                小明(qu_id:789): 南门搞不好堵车，咱们要不北门吧？
                小红(qu_id:101): 中！
                小丽(qu_id:666): 6啊你们俩，去公园不带我吗？
                小红(qu_id:101): 那不能，一起去吧！

                """
    # Desired structure
    desired_structure = {
        "activity": {
            "activity_id": "",
            "start_time": "",
            "end_time": "",
            "location": {
                "address": "",
                "latitude": "",
                "longitude": ""
            },
            "participants": [
                {
                    "name": "",
                    "qu_id": "",
                    "tasks": []
                },
            ],
            "description": "",
            "tags": []
        }
    }
    conversation_message = prompt_str + conversation_content
    poluted_json = call_llm_with_messages(conversation_message)
    purified_json = purify_json(poluted_json)
    print(purified_json)
    transformed_json = transform_json(purified_json,desired_structure)
    print(transformed_json)
