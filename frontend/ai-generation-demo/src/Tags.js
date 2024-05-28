import React from 'react';
import './css/Tags.css';

const Tags = (tags) => {
  // console.log(tags.tags)
  return (
    <div className="tags">
      {tags.tags.map((tag, index) => (
        <span key={index} className="tag">
          {tag}
        </span>
      ))}

    </div>
  );
};

export default Tags;
