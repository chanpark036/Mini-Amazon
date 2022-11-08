
import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'


function App() {
  const [getMessage, setGetMessage] = useState([]);
  useEffect(()=>{
    fetch('http://localhost:5000/',{
      'methods':'GET',
      headers : {
        'Content-Type':'application/json'
      }
    })
    .then(response => response.json())
    .then(response => setGetMessage(response))
    .catch(error => console.log(error))

  },[])

  
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>React</p>
        <div>{getMessage.status === 200 ? 
          <h3>{getMessage.avail_products}</h3>
          :
          <h3>LOADING</h3>}</div>
      </header>
    </div>
  );
}

export default App;