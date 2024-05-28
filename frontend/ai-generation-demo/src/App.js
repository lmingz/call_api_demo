import Event from './Event.js'
import './css/App.css';
import React, { useEffect, useState } from 'react';

const App = () => {
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
  
  const [eventData, setEventData] = useState(initData);

  useEffect(() => {
    // This will run after eventData has been updated
    console.log("eventData from APP (after setEventData):", JSON.stringify(eventData, null, 2));
  }, [eventData]);

  const fetchEventData = async () => {
    console.log("button clicked");
    const url = 'http://127.0.0.1:5000/generate_event?prompt_str=请帮我总结如下对话，生成活动标题，并填充如下json数据结构%20{%20%22event%22:%20{%20%22event_title%22:%20%22%22,%20%22start_time%22:%20%22%22,%20%22end_time%22:%20%22%22,%20%22location%22:%20{%20%22address%22:%20%22%22,%20%22latitude%22:%20%22longitude%22:%20},%20%22participants%22:%20[%20{%20%22name%22:%20%22%22,%20%22qu_id%22:%20%22%22,%20%22tasks%22:%20[]%20},%20],%20%22description%22:%20%22%22,%20%22tags%22:%20[%20]%20}%20}%20注意请仅仅返回json本身！不要返回其他任何字符！对于event_title字段，请为本活动归纳一个标题。对于tags这一field，请根据对话内容生成合适的tag,tag请使用中文。请至少生成3个tag。%20如果对话中决定了某个人在活动中的任务，请在“description”中列出。请确保不要在JSON中增加任何新字段。%20对话：&conversation_content=小明(qu_id:789):%20小红，我们明天上午一起去公园野餐怎么样？%20小红(qu_id:101):%20好啊！我们去人民公园吧，早上10点怎么样？%20小明(qu_id:789):%2010点太早了，11点可以吗？我们在哪里见面？%20小红(qu_id:101):%20好的，11点在人民公园南门见面吧%20小明(qu_id:789):%20南门搞不好堵车，咱们要不北门吧？%20小红(qu_id:101):%20中！%20小丽(qu_id:666):%206啊你们俩，去公园不带我吗？%20小红(qu_id:101):%20那不能，一起去吧！';
    
    try {
      const response = await fetch(url);
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
      <button onClick={fetchEventData}>
        generate event
      </button>
      <div>
        <h1>{eventData.event.event_title}</h1>
        <p>Start Time: {eventData.event.start_time}</p>
        <p>End Time: {eventData.event.end_time}</p>
        <p>Location: {eventData.event.location.address}</p>
        <p>Description: {eventData.event.description}</p>
        <h2>Participants</h2>
        <ul>
          {eventData.event.participants.map((participant, index) => (
            <li key={index}>{participant.name} (ID: {participant.qu_id})</li>
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
