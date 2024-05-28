import React from 'react';
import './css//EventCard.css';

const EventCard = ({ children }) => {
  return <div className="card">{children}</div>;
};

export default EventCard;
