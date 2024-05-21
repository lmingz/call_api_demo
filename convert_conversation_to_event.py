import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
import re
import json


def call_llm_with_messages(message):
    messages = [
        {"role": "system", "content": "assistant"},
        {"role": "user", "content": message},
    ]
    response = Generation.call(
        model="qwen-72b-chat",
        messages=messages,
        # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
        seed=250,
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
                注意请仅仅返回json本身，不要返回其他任何字符。对于tag这一field，请根据对话内容生成合适的tag,tag请使用中文。
                如果对话中决定了某个人在活动中的任务，请在“description”中列出。请确保不要在JSON中增加任何新字段。
                对话：
                """
    conversation_content = """
                小明(qu_id:789): 大家，我计划下个月去泰国旅游，有没有人想加入？
                小红(qu_id:101): 哇，听起来好棒！我一定要去！
                小强(qu_id:102): 我也去，泰国的美食我期待很久了。
                小丽(qu_id:666): 算我一个，我超想去看泰国的海滩。
                小华(qu_id:103): 我也要加入，我们可以一起去浮潜。
                小刚(qu_id:104): 我负责规划行程和预订酒店，大家有什么特别想去的地方吗？
                小敏(qu_id:105): 我想去清迈看看古城，听说那里很有特色。
                小芳(qu_id:106): 曼谷的夜市我一定要去逛逛。
                小兰(qu_id:107): 我听说普吉岛的海滩很美，我们一定要去。
                小梅(qu_id:108): 我想去体验一下泰国的按摩，听说很放松。
                小菊(qu_id:109): 我来做我们的财务，保证我们的旅行预算合理。
                小明(qu_id:789): 我们这次旅行的预算是多少？大家有什么建议？
                小红(qu_id:101): 我觉得每人预算5000元应该差不多。
                小强(qu_id:102): 包括机票和酒店吗？我们要不要找个旅行团？
                小丽(qu_id:666): 我觉得自由行更自由，我们可以自己安排行程。
                小华(qu_id:103): 我同意，我们可以自己订机票和酒店。
                小刚(qu_id:104): 我会提前查好机票和酒店的价格，给大家一个参考。
                小敏(qu_id:105): 我们要不要考虑租车？这样出行更方便。
                小芳(qu_id:106): 好主意，我们可以轮流开车。
                小兰(qu_id:107): 我们还要准备一些旅行保险，以防万一。
                小梅(qu_id:108): 对，安全第一。
                小菊(qu_id:109): 我会负责收集大家的意见，然后统一安排。

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
