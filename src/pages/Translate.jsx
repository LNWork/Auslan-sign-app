import React, { useState } from 'react';

// Language options (for demo purposes, a small set of languages)
const languages = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  { code: 'de', name: 'German' },
  { code: 'zh', name: 'Chinese' },
];

const TranslateApp = () => {
  const [sourceText, setSourceText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('es');

  // This is where your translation logic would go, such as calling an API
  const handleTranslate = () => {
    // Example translation logic (to be replaced with real translation logic/API)
    setTranslatedText(`Translated (${targetLang}): ${sourceText}`);
  };

  // Swap languages
  const handleSwapLanguages = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
  };

  return (
    <div style={styles.container}>
      <div style={styles.panel}>
        <h2>Source</h2>
        <select 
          value={sourceLang} 
          onChange={(e) => setSourceLang(e.target.value)} 
          style={styles.dropdown}
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
        <textarea
          placeholder="Enter text"
          value={sourceText}
          onChange={(e) => setSourceText(e.target.value)}
          style={styles.textarea}
        />
      </div>

      <div style={styles.buttons}>
        <button onClick={handleSwapLanguages} style={styles.button}>Swap Languages</button>
        <button onClick={handleTranslate} style={styles.button}>Translate</button>
      </div>

      <div style={styles.panel}>
        <h2>Target</h2>
        <select 
          value={targetLang} 
          onChange={(e) => setTargetLang(e.target.value)} 
          style={styles.dropdown}
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
        <textarea
          placeholder="Translation will appear here"
          value={translatedText}
          readOnly
          style={styles.textarea}
        />
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row', // Align panels side by side
    alignItems: 'center',
    justifyContent: 'space-between', // Add spacing between panels
    gap: '20px',
    width: '80%',
    margin: '0 auto',
  },
  panel: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '45%', // Ensure each panel takes up equal space
  },
  dropdown: {
    width: '100%',
    padding: '10px',
    marginBottom: '10px',
    fontSize: '16px',
  },
  textarea: {
    width: '100%',
    height: '150px',
    padding: '10px',
    fontSize: '16px',
    resize: 'none',
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
};

export default TranslateApp;
