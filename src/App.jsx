import React from 'react';
import ReactDOM from 'react-dom';
// import './index.css';  // Import any CSS if needed
import Translate from './pages/translate';

function App() {
  return (
    <div>
      <h1>Welcome to the React App</h1>
      <Translate />   {/* Add Translate component */}
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
