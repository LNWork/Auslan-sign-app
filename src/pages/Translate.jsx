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
  const get_sign_trans = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8001/get_sign_to_text', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      
      // Output parsed sentence to console
      console.log('Full response:', data);

      // Set translated text or handle fallback
      const translatedText = data.translation;
      setTranslatedText(translatedText);

    } catch (error) {
      console.error('Error:', error);
      setTranslatedText(`Error: ${error.message}. Please check the API and input.`);
    }
  }

  setInterval(get_sign_trans(), 1000);

  // Function to convert text to video
  const handleTextToVideo = async () => {
    const fixedSourceText = sourceText.trim();
    console.log('Sending Source Text:', fixedSourceText);

    // 1. API call to parse sentence to Auslan grammar
    try {
      const response = await fetch('http://3.106.229.4:5000/t2s', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ t2s_input: fixedSourceText }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      
      // Output parsed sentence to console
      console.log('Full response:', data);

      // Set translated text or handle fallback
      const translatedText = data.Translated_text || data.translatedText || (Array.isArray(data.queries) ? data.queries.join(', ') : 'No translation available.');
      setTranslatedText(translatedText);

      

    } catch (error) {
      console.error('Error:', error);
      setTranslatedText(`Error: ${error.message}. Please check the API and input.`);
    }

    // 2. Firebase - fetch the sign language video based on the translated text
    try {
      const videoPath = getVideoPathForText(fixedSourceText);
      const videoRef = ref(storage, videoPath);
      const videoUrl = await getDownloadURL(videoRef);
      setAnimatedSignVideo(videoUrl);
    } catch (error) {
      console.error('Error fetching video:', error);
    }
  };

    // Mock function to map user input to a specific video path in Firebase
    const getVideoPathForText = (inputText) => {
      return 'gs://auslan-194e5.appspot.com/output_videos/I absolutely enjoy basketball.mp4';  // Default video path
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

          {/* <div style={styles.panel}>
            <h2>Auslan Sentence</h2>
            <textarea
              placeholder="Auslan sentence will appear here"
              value={translatedText}
              readOnly
              style={styles.textarea}
            />
          </div> */}

          <div style={styles.panel}>
            <h2>Sign Video</h2>
            {animatedSignVideo ? (
              <div style={styles.videoContainer}>
                <video
                  src={animatedSignVideo}
                  controls
                  autoPlay
                  loop
                  style={styles.video}
                  onLoadedMetadata={(e) => e.target.playbackRate = 2.0}
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
    width: '600px',
    height: '600px',
    boxSizing: 'border-box',
  },
  textarea: {
    width: '600px',
    height: '600px',
    padding: '10px',
    fontSize: '20px',
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
    fontSize: '20px',
    cursor: 'pointer',
  },
  videoContainer: {
    width: '100%', // Or any desired percentage of the parent width
    maxWidth: '800px', // Set a maximum width
    height: 'auto', // Let the height adjust based on the aspect ratio
    display: 'flex',
    justifyContent: 'center', // Center the video horizontally
    alignItems: 'center', // Center the video vertically
    overflow: 'hidden', // Hide any overflow in case the video exceeds the container
  },
  video: {
    width: '100%', // Video will take up the full width of the container
    height: 'auto', // Maintain the aspect ratio by adjusting height automatically
    objectFit: 'contain', // Ensure the video fits within the container without stretching
  },
  videoPlaceholder: {
    width: '600px', // Full width placeholder
    height: '600px', // Set a height for the placeholder
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ccc', // A background color for the placeholder
  },
};

export default TranslateApp;