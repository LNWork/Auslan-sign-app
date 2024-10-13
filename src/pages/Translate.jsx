import React, { useState } from 'react';
import VideoInput from '../components/VideoInput';

const TranslateApp = () => {
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');

  // This is where your translation logic would go, such as calling an API
  const handleTranslate = () => {
    // Example translation logic (to be replaced with real translation logic/API)
    setTranslatedText(`Translated Text: ${sourceText}`);
  };

  return (
    <div style={styles.container}>
      <div style={styles.panel}>
        <h2>Sign</h2>
        {/* VideoInput component for video capture */}
        <VideoInput />
      </div>

      <div style={styles.buttons}>
        <button onClick={handleTranslate} style={styles.button}>Translate</button>
      </div>

      <div style={styles.panel}>
        <h2>Text</h2>
        <textarea
          placeholder="Translation will appear here"
          value={translatedText}
          readOnly
          style={styles.textarea}
        />
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row', // Align panels side by side
    alignItems: 'center',
    justifyContent: 'space-between', // Add spacing between panels
    gap: '20px',
    width: '100%',
    margin: '0 auto',
  },
  panel: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '50%', // Ensure each panel takes up equal space
    height: '550px', // Taller height for both panels (adjust as needed)
  },
  textarea: {
    width: '100%',
    height: '100%', // Match height with the VideoInput panel
    padding: '10px',
    fontSize: '16px',
    resize: 'none', // Prevent manual resizing of the textarea
    boxSizing: 'border-box', // Ensure padding is included within the size
  },
  buttons: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '10px',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
  },
};

export default TranslateApp;
