import React from 'react';
import './Participants.css';

const Participants = () => {
  return (
    <div className="participants">
      <img src="avatar1.png" alt="avatar" className="avatar" />
      <img src="avatar2.png" alt="avatar" className="avatar" />
      <span>4/10人已参加 · <strong>邀请朋友</strong></span>
      <span>@天津大学西门体育场 · <strong>修改地址</strong> · 添加时间</span>
    </div>
  );
};

export default Participants;
