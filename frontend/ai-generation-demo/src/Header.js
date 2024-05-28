import React from 'react';
import './css//Header.css';

const Header = (title) => {
  // console.log("from header" + title.title);
  return (
    <div className="header">
      <h1>{title.title}</h1>
      <div className="options">•••</div>
    </div>
  );
};

export default Header;