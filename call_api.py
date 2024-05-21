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
        model="qwen-max",
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
                            "qu_id": ""
                        },
                        
                        ],
                        "description": "",
                        "tags": [
                        
                        ]
                    }
                }
                注意请仅仅返回json本身，不要返回其他任何字符。对于tag这一field，请根据对话内容生成合适的tag,tag请使用中文。
                如果对话中决定了某个人在活动中的任务，请在“description”中列出。
                对话：
                """
    conversation_content = """
                小明(qu_id:789): 嘿，我听说市中心新开了一家特别火的日料店叫kuka，但朋友们都没空，有人想一起去吗？
                小华(qu_id:103): 真的吗？我也一直想去尝尝，但也是一个人，可以加入你吗？
                小明(qu_id:789): 当然可以，人多热闹。我们什么时候去？
                小华(qu_id:103): 这周六下午怎么样？我那天有空。
                小红(qu_id:101): 我在社交媒体上看到有人分享那家日料店的照片，看起来好诱人，我也想去。
                小明(qu_id:789): 看来我们有共同的兴趣，小红，你周六有空吗？我们可以一起去。
                小红(qu_id:101): 周六我可以，太好了，终于有人陪我一起去了。
                小刚(qu_id:104): 我也看到了那家日料店的帖子，想去很久了，你们介意我加入吗？
                小明(qu_id:789): 当然不介意，小刚，欢迎加入我们的小队。
                小刚(qu_id:104): 谢谢，我听说那里的寿司很有名，我一定要尝尝。
                小丽(qu_id:666): 你们都去那家日料店吗？我也一个人，可以和你们一起去吗？
                小红(qu_id:101): 当然可以，小丽，我们的队伍越来越壮大了。
                小丽(qu_id:666): 太好了，我听说那里的清酒也很有特色，我们可以一起尝尝。
                小明(qu_id:789): 既然我们都决定周六去，我们要不要定个具体时间？
                小华(qu_id:103): 我觉得下午两点去不错，人不会太多，我们可以慢慢享受。
                小红(qu_id:101): 听起来不错，我们去之前要不要先在餐厅门口集合？
                小刚(qu_id:104): 好主意，我们可以在门口先互相认识一下。
                小丽(qu_id:666): 那我们就周六下午两点，在餐厅门口集合吧。
                小明(qu_id:789): 我们要不要提前订位？我怕到时候人多要等。
                小华(qu_id:103): 好主意，我来联系一下餐厅，看看能不能预订。
                小红(qu_id:101): 顺便问问他们有没有特别的推荐菜品。
                小刚(qu_id:104): 对，问问他们的招牌菜是什么？
                小丽(qu_id:666): 我也可以帮忙，看看有没有优惠信息。
                """
    conversation_message = prompt_str + conversation_content
    poluted_json = call_llm_with_messages(conversation_message)
    purified_json = purify_json(poluted_json)
    print(purified_json)
