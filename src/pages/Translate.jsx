import React, { useState } from 'react';
import VideoInput from '../components/VideoInput';

const TranslateApp = () => {
  const [mode, setMode] = useState('videoToText');
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [animatedSignVideo, setAnimatedSignVideo] = useState(null);

  // Function to swap between modes
  const handleSwap = () => {
    setAnimatedSignVideo(null);
    setMode((prevMode) => (prevMode === 'videoToText' ? 'textToVideo' : 'videoToText'));
  };

  // Function to convert text to video
  const handleTextToVideo = async () => {
    const fixedSourceText = sourceText.trim(); // Ensure there's no leading/trailing whitespace
    console.log('Sending Source Text:', fixedSourceText);

    try {
      // Send the text to the Flask endpoint
      const response = await fetch('http://54.167.220.178:5000/api/text_to_animation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ t2s_input: fixedSourceText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('API Response:', data);

      if (data.status === "success") {
        setTranslatedText(data.message); // Assuming the response contains a success message
        // Here you would also handle setting the video URL if the response contains it
        // For instance, if the message contains a video URL, set it like this:
        // setAnimatedSignVideo(data.videoUrl); // Adjust as needed based on your response structure
      } else {
        setTranslatedText('No translation available.');
      }

    } catch (error) {
      console.error('Error details:', error);
      setTranslatedText(`Error: ${error.message}. Please check the API and input.`);
    }
  };

  return (
    <div style={styles.container}>
      {mode === 'videoToText' ? (
        <>
          <div style={styles.panel}>
            <h2>Sign</h2>
            <VideoInput />
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
              <div style={styles.videoPlaceholder}>
                <video src={animatedSignVideo} controls />
              </div>
            ) : (
              <div style={styles.videoPlaceholder}>Sign language animation will appear here</div>
            )}
          </div>

          <div style={styles.panel}>
            <h2>API Response</h2>
            <textarea
              placeholder="API response will appear here"
              value={translatedText}
              readOnly
              style={styles.textarea}
            />
          </div>
        </>
      )}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '20px',
    width: '100%',
    margin: '0 auto',
  },
  panel: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    width: '45%',
    height: '400px',
    boxSizing: 'border-box',
  },
  textarea: {
    width: '100%',
    height: '100%',
    padding: '10px',
    fontSize: '16px',
    resize: 'none',
    boxSizing: 'border-box',
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
    height: '100%',
    backgroundColor: '#ddd',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontSize: '16px',
    boxSizing: 'border-box',
  },
};

export default TranslateApp;
