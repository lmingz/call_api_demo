import React from 'react';
import EventCard from './EventCard';
import Header from './Header';
import Description from './Description';
import Tags from './Tags';
import Participants from './Participants';
import Footer from './Footer';
import './css//Event.css';


const Event = (eventData) => {
  console.log("from Event: " + JSON.stringify(eventData, null, 2))
  console.log("from Event：" + eventData.event_title)
  return (
    <div className="event">
      <h1></h1>
      <EventCard>
        <Header title={eventData.event_title}/>
        <Description description = {eventData.description} />
        {/* <Tags tags = {eventData.tags}/> */}
        <Participants event = {eventData}/>
        <Footer />
      </EventCard>
    </div>
  );
};

export default Event;
