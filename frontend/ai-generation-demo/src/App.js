//import Event from './Event.js'
import './css/App.css';
// import Event from './Event'
import React, { useEffect, useState } from 'react';

const initData = {
  event: {
    event_title: '默认标题',
    start_time: '2022-04-09 11:00:00',
    end_time: '2022-04-09 12:00:00',
    location: { address: '默认地点' },
    participants: [{ name: '默认名字', qu_id: '默认ID', tasks: [] }],
    description: '默认事件描述，默认事件描述，默认事件描述，默认事件描述，默认事件描述，默认事件描述，默认事件描述，默认事件描述',
    tags: ['标签1', '标签2', '标签3']
  }
};
const generateEventPrompt = `
请帮我根据如下对话讨论，填充如下json数据结构:
{
  "event": {
    "event_title": "",
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
      }
    ],
    "description": "",
    "tags": []
  }
}
注意请仅仅返回json本身！不要返回其他任何字符！
对于event_title字段，请为本活动归纳一个标题。
对于description字段，请为本活动生成一个详略得当的描述。
对于tags这一field，请根据对话内容生成合适的tag,tag请使用中文。请至少生成3个tag,如果活动复杂请生成更多。
如果对话中决定了某个人即将在活动中承担的任务，请在这个人的“tasks”中列出。
`;

const App = () => {
  const [eventData, setEventData] = useState(initData);
  const [eventConversationContent, setEventConversationContent] = useState(`
  小明(qu_id:789): 小红，我们明天上午一起去公园野餐怎么样？
  小红(qu_id:101): 好啊！我们去人民公园吧，早上10点怎么样？
  小明(qu_id:789): 10点太早了，11点可以吗？我们在哪里见面？
  小红(qu_id:101): 好的，11点在人民公园南门见面吧
  小明(qu_id:789): 南门搞不好堵车，咱们要不北门吧？
  小红(qu_id:101): 中！
  小丽(qu_id:666): 6啊你们俩，去公园不带我吗？
  小红(qu_id:101): 那不能，一起去吧！`);
  const [latency, setLatency] = useState(null);


  useEffect(() => {
    // This will run after eventData has been updated
    console.log("eventData from APP (after setEventData):", JSON.stringify(eventData, null, 2));
  }, [eventData]);

  const fetchEventData = async () => {
    console.log("button clicked");
    const startTime = Date.now();
    const url = `http://127.0.0.1:5000/generate_event?prompt_str=${encodeURIComponent(generateEventPrompt)}&conversation_content=${encodeURIComponent(eventConversationContent)}`;

    try {
      const response = await fetch(url);
      const endTime = Date.now();
      const latency = endTime - startTime;
      setLatency(latency);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log("data from APP :" + JSON.stringify(data, null, 2));
      setEventData({ event: data.event });
    } catch (error) {
      console.error('Error fetching the event data:', error);
    }
  };

  return (
    <div className="app">
      <div>
        <textarea
          value={eventConversationContent}
          onChange={(e) => setEventConversationContent(e.target.value)}
          placeholder="请输入对话内容"
          rows="30"
          cols="50"
        />
      </div>
      <button onClick={fetchEventData}>
        generate event
      </button>
      <div>
        {latency !== null && <p>Request Latency: {latency} ms</p>}
      </div>
      <div>
        {/* <Event eventData = {eventData.event}/> */}
        <h1>{eventData.event.event_title}</h1>
        <p>Start Time: {eventData.event.start_time}</p>
        <p>End Time: {eventData.event.end_time}</p>
        <p>Location: {eventData.event.location.address}</p>
        <p>Description: {eventData.event.description}</p>
        <h2>Participants</h2>
        <ul>
          {eventData.event.participants.map((participant, index) => (
            <li key={index}>
              {participant.name} (ID: {participant.qu_id})
              {participant.tasks.length > 0 && (
                <ul>
                  {participant.tasks.map((task, taskIndex) => (
                    <li key={taskIndex}>{task}</li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
        <h2>Tags</h2>
        <ul>
          {eventData.event.tags.map((tag, index) => (
            <li key={index}>{tag}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
