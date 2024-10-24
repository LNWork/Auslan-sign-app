import React, { useState } from 'react';
import { storage, ref, getDownloadURL } from '../firebase';

const TranslateApp = () => {
  const [sourceText, setSourceText] = useState('');
  const [animatedSignVideo, setAnimatedSignVideo] = useState(null);

  // Mock function to map user input to a specific video path in Firebase
  const getVideoPathForText = (inputText) => {
    // Example: Simple mock mapping for testing purposes
    if (inputText.toLowerCase() === 'hello') {
      return 'gs://auslan-194e5.appspot.com/hello.mp4';  // Replace with your actual video path in Firebase
    } else if (inputText.toLowerCase() === 'thank you') {
      return 'gs://auslan-194e5.appspot.com/thankyou.mp4';  // Replace with another video path
    } else {
      return 'gs://auslan-194e5.appspot.com/test_video_FINAL.mp4';  // Default video path
    }
  };

  // Function to fetch the video based on user input
  const handleTextToVideo = async () => {
    const videoPath = getVideoPathForText(sourceText); // Get the Firebase video path based on the input text

    try {
      const videoRef = ref(storage, videoPath); // Reference to the video in Firebase
      const videoUrl = await getDownloadURL(videoRef); // Get the video URL from Firebase
      setAnimatedSignVideo(videoUrl); // Set the video URL to display the video
    } catch (error) {
      console.error('Error fetching video:', error);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.panel}>
        <h2>Text</h2>
        <textarea
          placeholder="Enter text to convert to sign language"
          value={sourceText}
          onChange={(e) => setSourceText(e.target.value)}
          style={styles.textarea}
        />
        <div style={styles.buttons}>
          <button onClick={handleTextToVideo} style={styles.button}>Convert</button>
        </div>
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
    height: '200px',
    padding: '10px',
    fontSize: '16px',
    resize: 'none',
  },
  buttons: {
    display: 'flex',
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
