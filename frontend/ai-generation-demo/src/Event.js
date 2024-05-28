import React from 'react';
import EventCard from './EventCard';
import Header from './Header';
import Description from './Description';
import Tags from './Tags';
import Participants from './Participants';
import Footer from './Footer';
import './css//Event.css';


const Event = (eventData) => {
  console.log("from event: " + eventData)
  return (
    <div className="event">
      <h1></h1>
      <EventCard>
        <Header title={eventData.event.event_title}/>
        <Description description = {eventData.event.description} />
        <Tags tags = {eventData.event.tags}/>
        <Participants event = {eventData.event}/>
        <Footer />
      </EventCard>
    </div>
  );
};

export default Event;
