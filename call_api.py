print ("hello")

import random
from http import HTTPStatus
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0


def call_with_messages():
    messages = [{'role': 'system', 'content': 'assistant'},
                {'role': 'user', 'content': '''
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
                小明(qu_id:789): 小红，我们明天上午一起去公园野餐怎么样？
                小红(qu_id:101): 好啊！我们去人民公园吧，早上10点怎么样？
                小明(qu_id:789): 10点太早了，11点可以吗？我们在哪里见面？
                小红(qu_id:101): 好的，11点在人民公园南门见面吧
                小明(qu_id:789): 南门搞不好堵车，咱们要不北门吧？
                小红(qu_id:101): 中！
                小丽(qu_id:666): 6啊你们俩，去公园不带我吗？
                小红(qu_id:101): 那不能，一起去吧！

                注意请仅仅返回json本身，不要返回其他任何字符。对于tag这一field，请根据对话内容生成合适的tag。
                 '''}]
    response = Generation.call(model="qwen-72b-chat",
                               messages=messages,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=114,
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()


# {
#   "activity": {
#     "activity_id": "123456",
#     "start_time": "2022-05-01T10:00:00",
#     "end_time": "2022-05-01T13:00:00",
#     "location": {
#       "address": "123 Main St, Anytown, USA",
#       "latitude": 37.7749,
#       "longitude": -122.4194
#     },
#     "participants": [
#       {
#         "name": "John Doe",
#         "qu_id": "123"
#       },
#       {
#         "name": "Jane Smith",
#         "qu_id": "456"
#       }
#     ],
#     "description": "Join us for a fun hiking trip to Mount Everest!",
#     "tags": [
#       "hiking",
#       "outdoor",
#       "adventure",
#       "team building"
#     ]
#   }
# }