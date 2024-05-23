import React from 'react';
import Card from './Card';
import Header from './Header';
import Description from './Description';
import Tags from './Tags';
import Participants from './Participants';
import Footer from './Footer';
import './App.css';

const App = () => {
  return (
    <div className="app">
      <Card>
        <Header />
        <Description />
        <Tags />
        <Participants />
        <Footer />
      </Card>
    </div>
  );
};

export default App;
