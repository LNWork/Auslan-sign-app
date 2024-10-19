import React from 'react'
import { useEffect, useState } from 'react';
import './App.css'
import TranslateApp from './pages/Translate'

const App = () => {
    return(
        <div>
            <h1 className="text-3xl font-bold underline">
                AuslanLive!
            </h1>
            <TranslateApp />
        </div>
    )
}

export default App