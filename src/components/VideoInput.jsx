import React, { useEffect, useRef, useState } from 'react';

// Import necessary MediaPipe scripts
const cameraUtilsUrl = "https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js";
const controlUtilsUrl = "https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js";
const drawingUtilsUrl = "https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js";
const holisticUrl = "https://cdn.jsdelivr.net/npm/@mediapipe/holistic/holistic.js";

// Load external MediaPipe scripts dynamically
const loadScript = (url) => {
  return new Promise((resolve) => {
    const script = document.createElement("script");
    script.src = url;
    script.crossOrigin = "anonymous";
    script.onload = () => resolve();
    document.head.appendChild(script);
  });
};

const VideoInput = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const resultsDivRef = useRef(null);
  const [error, setError] = useState(null); // State to handle errors
  
  useEffect(() => {
    // Load all necessary MediaPipe scripts
    const loadMediaPipe = async () => {
      try {
        await loadScript(cameraUtilsUrl);
        await loadScript(controlUtilsUrl);
        await loadScript(drawingUtilsUrl);
        await loadScript(holisticUrl);

        const videoElement = videoRef.current;
        const canvasElement = canvasRef.current;
        const canvasCtx = canvasElement.getContext('2d');
        const resultsDiv = resultsDivRef.current;

        const holistic = new window.Holistic({
          locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`,
        });

        holistic.setOptions({
          modelComplexity: 1,
          smoothLandmarks: true,
          enableSegmentation: true,
          smoothSegmentation: true,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5,
        });

        holistic.onResults((results) => {
          // Clear and prepare canvas
          canvasCtx.save();
          canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
          canvasCtx.globalCompositeOperation = 'destination-atop';
          canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
          canvasCtx.globalCompositeOperation = 'source-over';

          // Draw Pose and Hands Landmarks
          if (results.poseLandmarks) {
            window.drawConnectors(canvasCtx, results.poseLandmarks, window.POSE_CONNECTIONS, {
              color: '#00FF00',
              lineWidth: 4,
            });
            window.drawLandmarks(canvasCtx, results.poseLandmarks, { color: '#FF0000', lineWidth: 2 });
          }
          if (results.leftHandLandmarks) {
            window.drawConnectors(canvasCtx, results.leftHandLandmarks, window.HAND_CONNECTIONS, {
              color: '#CC0000',
              lineWidth: 5,
            });
            window.drawLandmarks(canvasCtx, results.leftHandLandmarks, { color: '#00FF00', lineWidth: 2 });
          }
          if (results.rightHandLandmarks) {
            window.drawConnectors(canvasCtx, results.rightHandLandmarks, window.HAND_CONNECTIONS, {
              color: '#00CC00',
              lineWidth: 5,
            });
            window.drawLandmarks(canvasCtx, results.rightHandLandmarks, { color: '#FF0000', lineWidth: 2 });
          }
          canvasCtx.restore();

          // Output Results to Page
          outputResults(results, resultsDiv);
        });

        const camera = new window.Camera(videoElement, {
          onFrame: async () => {
            await holistic.send({ image: videoElement });
          },
          width: 1280,
          height: 720,
        });
        camera.start();
      } catch (err) {
        if (err.name === 'NotAllowedError') {
          setError('Camera access was denied. Please allow camera permissions in your browser.');
        } else if (err.name === 'NotFoundError') {
          setError('No camera found. Please connect a camera to use this feature.');
        } else {
          setError(`Error accessing camera: ${err.message}`);
        }
      }
    };

    loadMediaPipe();

    // Cleanup on component unmount
    return () => {
      const scripts = document.querySelectorAll('script[src*="mediapipe"]');
      scripts.forEach((script) => script.remove());
    };
  }, []);

  const outputResults = (results, resultsDiv) => {
    let outputText = '<strong>Landmark Coordinates:</strong><br>';

    // Pose Landmarks
    if (results.poseLandmarks) {
      results.poseLandmarks.forEach((landmark, index) => {
        outputText += `Pose Landmark ${index}: (X: ${landmark.x.toFixed(3)}, Y: ${landmark.y.toFixed(3)}, Z: ${landmark.z.toFixed(3)})<br>`;
      });
    }

    // Left Hand Landmarks
    if (results.leftHandLandmarks) {
      outputText += '<br><strong>Left Hand Landmarks:</strong><br>';
      results.leftHandLandmarks.forEach((landmark, index) => {
        outputText += `Left Hand Landmark ${index}: (X: ${landmark.x.toFixed(3)}, Y: ${landmark.y.toFixed(3)}, Z: ${landmark.z.toFixed(3)})<br>`;
      });
    }

    // Right Hand Landmarks
    if (results.rightHandLandmarks) {
      outputText += '<br><strong>Right Hand Landmarks:</strong><br>';
      results.rightHandLandmarks.forEach((landmark, index) => {
        outputText += `Right Hand Landmark ${index}: (X: ${landmark.x.toFixed(3)}, Y: ${landmark.y.toFixed(3)}, Z: ${landmark.z.toFixed(3)})<br>`;
      });
    }

    // Update the resultsDiv with the generated outputText
    resultsDiv.innerHTML = outputText;
  };

  return (
    <div className="container" style={{ position: 'relative', width: '1280px', height: '720px' }}>
      {error ? (
        <div style={{ color: 'red' }}>{error}</div>
      ) : (
        <>
          <video ref={videoRef} className="input_video" style={{ display: 'none' }}></video>
          <canvas ref={canvasRef} className="output_canvas" width="1280" height="720" />
          <div className="results" ref={resultsDivRef} style={styles.results}></div>
        </>
      )}
    </div>
  );
};

const styles = {
  results: {
    position: 'absolute',
    top: '10px',
    left: '10px',
    color: 'white',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    padding: '10px',
    borderRadius: '5px',
    zIndex: 10, // Ensures it appears above the video/canvas
    fontFamily: 'Arial, sans-serif',
  },
};

export default VideoInput;