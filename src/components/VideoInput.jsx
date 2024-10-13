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
  const cameraRef = useRef(null); // Reference to the camera object
  const holisticRef = useRef(null); // Reference to the holistic object
  const [isCameraOn, setIsCameraOn] = useState(false); // State to track if the camera is on
  const [error, setError] = useState(null); // State to handle errors
  
  useEffect(() => {
    // Load MediaPipe scripts once and initialize the Holistic model
    const loadMediaPipe = async () => {
      await loadScript(cameraUtilsUrl);
      await loadScript(controlUtilsUrl);
      await loadScript(drawingUtilsUrl);
      await loadScript(holisticUrl);

      // Initialize holistic once
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

      // Store the holistic instance in a ref to reuse
      holisticRef.current = holistic;
    };

    loadMediaPipe();

    // Cleanup on component unmount to stop video stream and model
    return () => {
      stopCamera();
    };
  }, []);

  const startCamera = async () => {
    try {
      const videoElement = videoRef.current;
      const canvasElement = canvasRef.current;
      const canvasCtx = canvasElement.getContext('2d');

      // Request camera feed
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoElement.srcObject = stream;

      // If holistic model is initialized, use it
      if (!holisticRef.current) {
        console.error('Holistic model is not initialized');
        return;
      }

      const holistic = holisticRef.current;

      holistic.onResults((results) => {
        // Clear and prepare canvas
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height); // Draw the video on the canvas
        
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
      });

      // Initialize camera only once
      if (!cameraRef.current) {
        const camera = new window.Camera(videoElement, {
          onFrame: async () => {
            await holistic.send({ image: videoElement });
          },
          width: 1280,
          height: 720,
        });
        cameraRef.current = camera;
      }

      // Start the camera
      cameraRef.current.start();
      setIsCameraOn(true);
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

  const stopCamera = () => {
    if (cameraRef.current) {
      cameraRef.current.stop();
      const stream = videoRef.current.srcObject;
      if (stream) {
        stream.getTracks().forEach(track => track.stop()); // Stop the camera stream
      }
      videoRef.current.srcObject = null;
      setIsCameraOn(false);

      // Clear the canvas when the camera is turned off
      const canvasElement = canvasRef.current;
      const canvasCtx = canvasElement.getContext('2d');
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height); // Clear the canvas
    }
  };

  const toggleCamera = () => {
    if (isCameraOn) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  return (
    <div className="container" style={styles.container}>
      {error ? (
        <div style={{ color: 'red' }}>{error}</div>
      ) : (
        <>
          {/* Hide the video element, it is only used to source the webcam feed */}
          <video ref={videoRef} className="input_video" style={{ display: 'none' }}></video>

          {/* Only the canvas will be visible with the video feed and annotations */}
          <canvas ref={canvasRef} className="output_canvas" width="1920" height="1080" style={styles.canvas} />

          <div className="results" style={styles.results}></div>
        </>
      )}
      <button onClick={toggleCamera} style={styles.button}>
        {isCameraOn ? 'Turn Camera Off' : 'Turn Camera On'}
      </button>
    </div>
  );
};

const styles = {
  container: {
    position: 'relative',
    width: '100%',
    height: '100%',
    padding: '1px',
    boxSizing: 'border-box',
    outline: '2px solid #007bff',
  },
  canvas: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    borderRadius: '10px',
    boxSizing: 'border-box',
  },
  results: {
    position: 'absolute',
    top: '10px',
    left: '10px',
    color: 'white',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    padding: '10px',
    borderRadius: '5px',
    zIndex: 10,
    fontFamily: 'Arial, sans-serif',
  },
  button: {
    position: 'absolute',
    bottom: '20px',
    left: '20px',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    zIndex: 11,
  },
};

export default VideoInput;
