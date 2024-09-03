import React, { useState } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

const Testingsomething = () => {
    const [inputMode, setInputMode] = useState('text'); 
    const [typedText, setTypedText] = useState('');

    const { transcript, resetTranscript, listening } = useSpeechRecognition();

    if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
        return <div>Your browser does not support speech recognition.</div>;
    }

    const handleTextChange = (e) => {
        setTypedText(e.target.value);
    };

    const toggleInputMode = (mode) => {
        setInputMode(mode);
        if (mode === 'speech') {
            SpeechRecognition.startListening({ continuous: true });
        } else {
            SpeechRecognition.stopListening();
            resetTranscript();
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.whiteBox}>
                <div style={styles.modeSelector}>
                    <button onClick={() => toggleInputMode('text')} disabled={inputMode === 'text'}>
                        Manual Typing
                    </button>
                    <button onClick={() => toggleInputMode('speech')} disabled={inputMode === 'speech'}>
                        Speech to Text
                    </button>
                </div>
                {inputMode === 'text' ? (
                    <textarea
                        style={styles.textInput}
                        value={typedText}
                        onChange={handleTextChange}
                        placeholder="Type your text here..."
                    />
                ) : (
                    <div style={styles.speechInput}>
                        <p>{listening ? 'Listening...' : 'Click the button to start speaking'}</p>
                        <p>{transcript}</p>
                    </div>
                )}
            </div>
            <div style={styles.lineBox}>
                <div style={styles.line}></div>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        marginTop: '40px', // Adjust this to position the first box slightly above the middle
    },
    whiteBox: {
        width: '100%',
        maxWidth: '600px',
        padding: '20px',
        backgroundColor: '#fff',
        borderRadius: '10px',
        boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        marginBottom: '20px',
    },
    modeSelector: {
        marginBottom: '20px',
    },
    textInput: {
        width: '100%',
        height: '150px',
        padding: '10px',
        borderRadius: '5px',
        border: '1px solid #ccc',
        fontSize: '16px',
    },
    speechInput: {
        minHeight: '150px',
        padding: '10px',
        borderRadius: '5px',
        border: '1px solid #ccc',
        fontSize: '16px',
        backgroundColor: '#f9f9f9',
    },
    lineBox: {
        width: '100%',
        maxWidth: '600px',
        padding: '20px',
        textAlign: 'center',
        position: 'relative',
    },
    line: {
        width: '100%',
        height: '1px',
        backgroundColor: '#000',
        position: 'absolute',
        top: '50%',
        left: '0',
        transform: 'translateY(-50%)',
    },
};

export default Testingsomething;
