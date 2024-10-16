import React, { useState } from 'react';
import VideoInput from '../components/VideoInput'; // Ensure this path is correct based on your project structure

const Translate = () => {
  const [mode, setMode] = useState('videoToText'); // Toggle between 'videoToText' and 'textToVideo'
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [animatedSignVideo, setAnimatedSignVideo] = useState(null); // Placeholder for the animated video output
  const [keypoints, setKeypoints] = useState([]);

  // Handle receiving keypoints from VideoInput component
  const handleKeypointsChange = (newKeypoints) => {
    setKeypoints((prevKeypoints) => [...prevKeypoints, newKeypoints]);

    // Prepare data to send
    const dataToSend = {
      keypoints: newKeypoints,
    };

    // Send keypoints data to backend
    fetch('http://127.0.0.1:5000/api/keypoints', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend), // Convert data to JSON
    })
    .then(response => response.json())
    .then(data => {
      console.log('Data saved successfully:', data);
    })
    .catch((error) => {
      console.error('Error saving data:', error);
    });
  };

  const handleSwap = () => {
    // Reset animatedSignVideo when switching modes
    setAnimatedSignVideo(null);
    setMode((prevMode) => (prevMode === 'videoToText' ? 'textToVideo' : 'videoToText'));
  };

  const handleTextToVideo = () => {
    // Placeholder logic to convert text to an animated sign language video
    setAnimatedSignVideo(`Animation for: ${sourceText}`); // For now, just display a placeholder
  };

  return (
    <div style={styles.container}>
      {mode === 'videoToText' ? (
        <>
          {/* Video to Text Mode */}
          <div style={styles.panel}>
            <h2>Sign</h2>
            <VideoInput onKeypointsChange={handleKeypointsChange} />
          </div>

          <div style={styles.buttons}>
            <button onClick={handleSwap} style={styles.button}>Swap</button>
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
        </>
      ) : (
        <>
          {/* Text to Video Mode */}
          <div style={styles.panel}>
            <h2>Text</h2>
            <textarea
              placeholder="Enter text to convert to sign language"
              value={sourceText}
              onChange={(e) => setSourceText(e.target.value)}
              style={styles.textarea}
            />
          </div>

          <div style={styles.buttons}>
            <button onClick={handleSwap} style={styles.button}>Swap</button>
            <button onClick={handleTextToVideo} style={styles.button}>Convert</button>
          </div>

          <div style={styles.panel}>
            <h2>Sign Video</h2>
            {animatedSignVideo ? (
              <div style={styles.videoPlaceholder}>{animatedSignVideo}</div> // Placeholder for the sign language animation
            ) : (
              <div style={styles.videoPlaceholder}>Sign language animation will appear here</div>
            )}
          </div>
        </>
      )}
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
    justifyContent: 'center', // Center content vertically
    width: '45%', // Ensure each panel takes up equal space
    height: '400px', // Consistent height for both modes (adjust as needed)
    boxSizing: 'border-box',
  },
  textarea: {
    width: '100%',
    height: '100%', // Match height with the video panel
    padding: '10px',
    fontSize: '16px',
    resize: 'none',
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
  videoPlaceholder: {
    width: '100%',
    height: '100%', // Match the height with textarea and video
    backgroundColor: '#ddd',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontSize: '16px',
    boxSizing: 'border-box',
  },
};

export default Translate;
