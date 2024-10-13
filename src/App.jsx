import React from 'react'
import './App.css'
import VideoInput from './components/VideoInput'

const App = () => {
    return(
        <div>
            <h1 className="text-3xl font-bold underline">
                Translate Auslan!
            </h1>
            <VideoInput />
        </div>
    )
}

export default App