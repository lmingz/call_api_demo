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
        model="qwen-turbo",
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




def transform_event_json(original, desired):
    transformed = desired.copy()
    
    transformed['event']['event_id'] = original['event'].get('event_id', "")
    transformed['event']['start_time'] = original['event'].get('start_time', "")
    transformed['event']['end_time'] = original['event'].get('end_time', "")
    
    location = original['event'].get('location', {})
    transformed['event']['location']['address'] = location.get('address', "")
    transformed['event']['location']['latitude'] = location.get('latitude', "")
    transformed['event']['location']['longitude'] = location.get('longitude', "")
    
    transformed['event']['participants'] = [
        {
            "name": p.get('name', ""),
            "qu_id": p.get('qu_id', ""),
            "tasks": p.get('tasks', [])
        } for p in original['event'].get('participants', [])
    ]
    
    transformed['event']['description'] = original['event'].get('description', "")
    transformed['event']['tags'] = original['event'].get('tags', [])
    
    return transformed



@app.route('/generate_event', methods=['GET'])
def generate_event():
    prompt_str = request.args.get('prompt_str')
    conversation_content = request.args.get('conversation_content')
    # Desired structure
    desired_structure = {
        "event": {
            "event_id": "",
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
    transformed_json = transform_event_json(purified_json,desired_structure)
    print(transformed_json)
    return jsonify(transformed_json)

if __name__ == "__main__":
    app.run(debug=True)
