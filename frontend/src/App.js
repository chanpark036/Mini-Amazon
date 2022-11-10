
//import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
//import axios from 'axios'


function App() {

  const [products, setproduct] = useState([]);
  useEffect(() => {
    fetch("/index")
    .then(response => response.json())
    .then(jsonData => {
      console.log(jsonData)
      setproduct(jsonData)
    })
  }, []);

  return (
      <div className="App">
          <header className="App-header">
              <h1>React and flask</h1>
              {/* Calling a data from setdata for showing */}
          </header>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100vh',
            }}
          >
          <tr class="center">
            {products && products.map((item)=>
                <tr>
                  <th>{item.id}</th>
                  <th>{item.name}</th>
                  <th>{item.price}</th>
                </tr>
                )}
          </tr>
          </div>
      </div>
  );
}


export default App;