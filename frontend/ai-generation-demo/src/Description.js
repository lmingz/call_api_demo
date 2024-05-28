import React from 'react';
import './css//Description.css';

const Description = (description) => {
  // console.log(description);
  return <p className="description">{description.description}</p>;
};

export default Description;
