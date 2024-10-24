import React, { useState } from 'react';
import VideoInput from '../components/VideoInput';
import { storage, ref, getDownloadURL } from '../firebase';

const TranslateApp = () => {
  const [mode, setMode] = useState('videoToText');
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [animatedSignVideo, setAnimatedSignVideo] = useState(null);

  // Function to swap between modes
  const handleSwap = () => {
    setTranslatedText(''); // Clear the translated text on swap
    setMode((prevMode) => (prevMode === 'videoToText' ? 'textToVideo' : 'videoToText'));
  };

  // Function to convert text to video
  const handleTextToVideo = async () => {
    const fixedSourceText = sourceText.trim(); // Ensure there's no leading/trailing whitespace
    console.log('Sending Source Text:', fixedSourceText);

    try {
      const response = await fetch('http://3.106.229.4:5000/t2s', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ t2s_input: fixedSourceText }), // Send input as t2s_input
      });

      const responseText = await response.text();
      console.log('Raw response:', responseText);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, body: ${responseText}`);
      }

      let data;
      try {
        data = JSON.parse(responseText);
        console.log('Full response:', data); // Log the full response for debugging
      } catch (parseError) {
        console.error('Error parsing JSON:', parseError);
        throw new Error('Invalid JSON response');
      }

      // Check for translated text or queries
      if (data.Translated_text) { // Use Translated_text (uppercase "T")
        setTranslatedText(data.Translated_text); // Set translated text based on the backend response
      } else if (data.translatedText) { // Check for translatedText as well
        setTranslatedText(data.translatedText);
      } else if (Array.isArray(data.queries) && data.queries.length > 0) {
        setTranslatedText(data.queries.join(', '));
      } else {
        setTranslatedText('No translation available.'); // This is a fallback message
      }

    } catch (error) {
      console.error('Error details:', error);
      setTranslatedText(`Error: ${error.message}. Please check the API and input.`);
    }

    // Fetch the video based on the translated text
    const videoPath = getVideoPathForText(sourceText); // Get the Firebase video path based on the input text
  
    try {
      const videoRef = ref(storage, videoPath); // Reference to the video in Firebase
      const videoUrl = await getDownloadURL(videoRef); // Get the video URL from Firebase
      setAnimatedSignVideo(videoUrl); // Set the video URL to display the video
    } catch (error) {
      console.error('Error fetching video:', error);
    }
  };

    // Mock function to map user input to a specific video path in Firebase
    const getVideoPathForText = (inputText) => {
      return 'gs://auslan-194e5.appspot.com/test_video_FINAL.mp4';  // Default video path
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
            <h2>API Response</h2>
            <textarea
              placeholder="API response will appear here"
              value={translatedText}
              readOnly
              style={styles.textarea}
            />
          </div>

          <div style={styles.panel}>
            <h2>Sign Video</h2>
            {animatedSignVideo ? (
              <div style={styles.videoPlaceholder}>
                <video
                  src={'gs://auslan-194e5.appspot.com/test_video_FINAL.mp4'}
                  controls
                  autoPlay
                  loop
                  style={styles.video}
                />
              </div>
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
};

export default TranslateApp;