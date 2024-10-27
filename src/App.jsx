// App.jsx
import React from 'react'
import './App.css'
import TranslateApp from './pages/Translate'

const App = () => {
    return(
        <div style={styles.page}>
            <h1 className="text-3xl font-bold underline">
                AuslanLive
            </h1>
            <TranslateApp />
        </div>
    )
}

const styles = {
    page: {
        backgroundColor: '#1a1a1a', // ChatGPT-like background color
        minHeight: '100vh', // Ensures it covers the full viewport height
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
    },
};

export default App
