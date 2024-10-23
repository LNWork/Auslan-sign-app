// import React, { useState } from 'react';
// import VideoInput from '../components/VideoInput';

// const TranslateApp = () => {
//   const [mode, setMode] = useState('videoToText');
//   const [sourceText, setSourceText] = useState('');
//   const [translatedText, setTranslatedText] = useState('');
//   const [animatedSignVideo, setAnimatedSignVideo] = useState(null);

//   // Function to swap between modes
//   const handleSwap = () => {
//     setAnimatedSignVideo(null);
//     setMode((prevMode) => (prevMode === 'videoToText' ? 'textToVideo' : 'videoToText'));
//   };
//   const handleTextToVideo = async () => {
//     const fixedSourceText = sourceText;
//     console.log('Sending Source Text:', fixedSourceText);
  
//     try {
//       const response = await fetch('http://54.167.220.178:5000/t2s', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },  
//         body: JSON.stringify({ t2s_input: fixedSourceText }),
//       });
  
//       const responseText = await response.text();
//       console.log('Raw response:', responseText);
  
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}, body: ${responseText}`);
//       }
  
//       let data;
//       try {
//         data = JSON.parse(responseText);
//         console.log('Full response:', data); // Log the full response for debugging
//       } catch (parseError) {
//         console.error('Error parsing JSON:', parseError);
//         throw new Error('Invalid JSON response');
//       }
  
//       // Check for translated text or queries
//       if (data.translatedText) {
//         setTranslatedText(data.translatedText);
//       } else if (Array.isArray(data.queries) && data.queries.length > 0) {
//         setTranslatedText(data.queries.join(', '));
//       } else {
//         setTranslatedText('No translation available.');
//       }
  
//     } catch (error) {
//       console.error('Error details:', error);
//       setTranslatedText(`Error: ${error.message}. Please check the API and input.`);
//     }
//   };
  

//   return (
//     <div style={styles.container}>
//       {mode === 'videoToText' ? (
//         <>
//           <div style={styles.panel}>
//             <h2>Sign</h2>
//             <VideoInput />
//           </div>

//           <div style={styles.buttons}>
//             <button onClick={handleSwap} style={styles.button}>Swap</button>
//           </div>

//           <div style={styles.panel}>
//             <h2>Text</h2>
//             <textarea
//               placeholder="Translation will appear here"
//               value={translatedText}
//               readOnly
//               style={styles.textarea}
//             />
//           </div>
//         </>
//       ) : (
//         <>
//           <div style={styles.panel}>
//             <h2>Text</h2>
//             <textarea
//               placeholder="Enter text to convert to sign language"
//               value={sourceText}
//               onChange={(e) => setSourceText(e.target.value)}
//               style={styles.textarea}
//             />
//           </div>

//           <div style={styles.buttons}>
//             <button onClick={handleSwap} style={styles.button}>Swap</button>
//             <button onClick={handleTextToVideo} style={styles.button}>Convert</button>
//           </div>

//           <div style={styles.panel}>
//             <h2>Sign Video</h2>
//             {animatedSignVideo ? (
//               <div style={styles.videoPlaceholder}>
//                 <video src={animatedSignVideo} controls />
//               </div>
//             ) : (
//               <div style={styles.videoPlaceholder}>Sign language animation will appear here</div>
//             )}
//           </div>

//           <div style={styles.panel}>
//             <h2>API Response</h2>
//             <textarea
//               placeholder="API response will appear here"
//               value={translatedText} // Show translated text or error messages
//               readOnly
//               style={styles.textarea}
//             />
//           </div>
//         </>
//       )}
//     </div>
//   );
// };

// const styles = {
//   container: {
//     display: 'flex',
//     flexDirection: 'row',
//     alignItems: 'center',
//     justifyContent: 'space-between',
//     gap: '20px',
//     width: '100%',
//     margin: '0 auto',
//   },
//   panel: {
//     display: 'flex',
//     flexDirection: 'column',
//     alignItems: 'center',
//     justifyContent: 'center',
//     width: '45%',
//     height: '400px',
//     boxSizing: 'border-box',
//   },
//   textarea: {
//     width: '100%',
//     height: '100%',
//     padding: '10px',
//     fontSize: '16px',
//     resize: 'none',
//     boxSizing: 'border-box',
//   },
//   buttons: {
//     display: 'flex',
//     flexDirection: 'column',
//     justifyContent: 'center',
//     alignItems: 'center',
//     gap: '10px',
//   },
//   button: {
//     padding: '10px 20px',
//     fontSize: '16px',
//     cursor: 'pointer',
//   },
//   videoPlaceholder: {
//     width: '100%',
//     height: '100%',
//     backgroundColor: '#ddd',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//     fontSize: '16px',
//     boxSizing: 'border-box',
//   },
// };

// export default TranslateApp;









// import React, { useState } from 'react';
// import VideoInput from '../components/VideoInput';

// const TranslateApp = () => {
//   const [mode, setMode] = useState('videoToText'); // Toggle between 'videoToText' and 'textToVideo'
//   const [sourceText, setSourceText] = useState('');
//   const [translatedText, setTranslatedText] = useState(''); // Presuming you will set translated text here
//   const [animatedSignVideo, setAnimatedSignVideo] = useState(null); // Placeholder for the animated video output
//   const [error, setError] = useState(null); // To store error messages
//   const [isLoading, setIsLoading] = useState(false); // Loading state

//   // Function to swap between modes
//   const handleSwap = () => {
//     setAnimatedSignVideo(null);
//     setError(null);
//     setSourceText(''); // Reset text field on swap
//     setMode((prevMode) => (prevMode === 'videoToText' ? 'textToVideo' : 'videoToText'));
//   };

//   // Function to handle text-to-video conversion
//   const handleTextToVideo = async () => {
//     try {
//       setError(null); // Reset error
//       setAnimatedSignVideo(null); // Reset video placeholder
//       setIsLoading(true); // Set loading state

//       const response = await fetch('http://localhost:5000/concatenate-video', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ sentence: sourceText }), // Send the entered text to the backend
//       });

//       if (!response.ok) {
//         throw new Error('Failed to connect to the backend');
//       }

//       const data = await response.json();

//       // Check if there are any missing words and display a message for that
//       if (data.missingWords && data.missingWords.length > 0) {
//         setError(`The following words are not in the database: ${data.missingWords.join(', ')}`);
//       }

//       // Set the video link if the concatenation was successful
//       if (data.videoUrl) {
//         setAnimatedSignVideo(data.videoUrl); // Assuming the backend returns a video URL
//       }
//     } catch (err) {
//       setError(`Error: ${err.message}`);
//     } finally {
//       setIsLoading(false); // Reset loading state
//     }
//   };

//   return (
//     <div style={styles.container}>
//       {mode === 'videoToText' ? (
//         <>
//           {/* Video to Text Mode */}
//           <div style={styles.panel}>
//             <h2>Sign</h2>
//             <VideoInput />
//           </div>

//           <div style={styles.buttons}>
//             <button onClick={handleSwap} style={styles.button}>Swap</button>
//           </div>

//           <div style={styles.panel}>
//             <h2>Text</h2>
//             <textarea
//               placeholder="Translation will appear here"
//               value={translatedText}
//               readOnly
//               style={styles.textarea}
//             />
//           </div>
//         </>
//       ) : (
//         <>
//           {/* Text to Video Mode */}
//           <div style={styles.panel}>
//             <h2>Text</h2>
//             <textarea
//               placeholder="Enter text to convert to sign language"
//               value={sourceText}
//               onChange={(e) => setSourceText(e.target.value)}
//               style={styles.textarea}
//               aria-label="Input text to convert to sign language" // Accessibility
//             />
//           </div>

//           <div style={styles.buttons}>
//             <button onClick={handleSwap} style={styles.button}>Swap</button>
//             <button onClick={handleTextToVideo} style={styles.button} disabled={isLoading}>
//               {isLoading ? 'Converting...' : 'Convert'}
//             </button>
//           </div>

//           <div style={styles.panel}>
//             <h2>Sign Video</h2>
//             {error && <div style={{ color: 'red' }}>{error}</div>} {/* Display error message if any */}
//             {animatedSignVideo ? (
//               <video style={styles.videoPlaceholder} controls>
//                 <source src={animatedSignVideo} type="video/mp4" />
//                 Your browser does not support the video tag.
//               </video> // Assuming the backend sends a video URL that can be used as the video source
//             ) : (
//               <div style={styles.videoPlaceholder}>Sign language animation will appear here</div>
//             )}
//           </div>
//         </>
//       )}
//     </div>
//   );
// };

// const styles = {
//   container: {
//     display: 'flex',
//     flexDirection: 'row',
//     alignItems: 'center',
//     justifyContent: 'space-between',
//     gap: '20px',
//     width: '100%',
//     margin: '0 auto',
//   },
//   panel: {
//     display: 'flex',
//     flexDirection: 'column',
//     alignItems: 'center',
//     justifyContent: 'center',
//     width: '45%',
//     height: '400px',
//     boxSizing: 'border-box',
//     border: '1px solid #ccc', // Add border for better visibility
//     padding: '10px',
//   },
//   textarea: {
//     width: '100%',
//     height: '100%',
//     padding: '10px',
//     fontSize: '16px',
//     resize: 'none',
//     boxSizing: 'border-box',
//   },
//   buttons: {
//     display: 'flex',
//     flexDirection: 'column',
//     justifyContent: 'center',
//     alignItems: 'center',
//     gap: '10px',
//   },
//   button: {
//     padding: '10px 20px',
//     fontSize: '16px',
//     cursor: 'pointer',
//     backgroundColor: '#007BFF',
//     color: '#fff',
//     border: 'none',
//     borderRadius: '4px',
//     transition: 'background-color 0.3s',
//   },
//   buttonDisabled: {
//     backgroundColor: '#ccc',
//     cursor: 'not-allowed',
//   },
//   videoPlaceholder: {
//     width: '100%',
//     height: '100%',
//     backgroundColor: '#ddd',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//     fontSize: '16px',
//     boxSizing: 'border-box',
//   },
// };

// export default TranslateApp;


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
    const fixedSourceText = sourceText;
    console.log('Sending Source Text:', fixedSourceText);

    try {
      const response = await fetch('http://54.167.220.178:5000/t2s', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ t2s_input: fixedSourceText }),
      });

      const responseText = await response.text();
      console.log('Raw response:', responseText);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, body: ${responseText}`);
      }

      let data;
      try {
        data = JSON.parse(responseText);
        console.log('Full response:', data);
      } catch (parseError) {
        console.error('Error parsing JSON:', parseError);
        throw new Error('Invalid JSON response');
      }

      if (data.translatedText) {
        setTranslatedText(data.translatedText);
      } else if (Array.isArray(data.queries) && data.queries.length > 0) {
        setTranslatedText(data.queries.join(', '));
      } else {
        setTranslatedText('No translation available.');
      }

    } catch (error) {
      console.error('Error details:', error);
      setTranslatedText(`Error: ${error.message}. Please check the API and input.`);
    }
  };

  // Function to run the Python script
  const handleRunPythonScript = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/run-python-script', {
        method: 'POST',
      });
  
      if (!response.ok) {
        throw new Error(`Error running Python script: ${response.statusText}`);
      }
  
      const result = await response.json();
      console.log('Python script output:', result);
      setTranslatedText('Python script ran successfully!');
    } catch (error) {
      console.error('Error:', error);
      setTranslatedText(`Error: ${error.message}.`);
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
            <button onClick={handleRunPythonScript} style={styles.button}>Python</button> {/* New Python Button */}
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