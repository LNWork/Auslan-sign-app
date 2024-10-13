import React from 'react'
import './App.css'
import VideoInput from './components/VideoInput'
import TranslateApp from './pages/Translate'

const App = () => {
    return(
        <div>
            <h1 className="text-3xl font-bold underline">
                Translate Auslan!
            </h1>
            {/* <VideoInput /> */}
            <TranslateApp />
        </div>
    )
}

export default App