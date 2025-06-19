import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [productTitle, setProductTitle] = useState('');
  const [history, setHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    let interval;
    if (loading) {
      setProgress(0);
      interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 98) return prev;
          return prev + Math.random() * 2;
        });
      }, 200);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleGenerate = async () => {
    if (!url) return;
    setLoading(true);
    setVideoUrl('');
    setProductTitle('');
    setErrorMsg('');

    try {
      const response = await axios.post('http://localhost:8000/generate', { url });
      if (response.data?.video_url) {
        setVideoUrl(response.data.video_url);
        setProductTitle(response.data.title || 'Your Video Ad');
        setProgress(100);
        setHistory(prev => [...prev, response.data.video_url]);
      } else {
        setErrorMsg('❌ Failed to generate video.');
      }
    } catch (error) {
      setErrorMsg('⚠️ Error generating video. Please try again.');
      console.error(error);
    } finally {
      setTimeout(() => setLoading(false), 400);
    }
  };

  const handlePasteClick = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setUrl(text);
    } catch (err) {
      alert('Clipboard access denied.');
    }
  };

  const toggleDark = () => {
    setDarkMode(!darkMode);
    document.body.className = darkMode ? '' : 'dark';
  };

  return (
    <div className="app-container">
      <h1>🛍️ AI Product Video Generator</h1>

      <div className="input-section">
        <input
          type="text"
          placeholder="Enter a product page URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button onClick={handlePasteClick}>📋 Paste</button>
        <button onClick={toggleDark}>{darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}</button>
      </div>

      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Video'}
      </button>

      {loading && (
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${progress}%` }}></div>
        </div>
      )}

      {errorMsg && <p className="error">{errorMsg}</p>}

      {videoUrl && (
        <div className="video-section">
          <h2>{productTitle}</h2>
          <video
            controls
            style={{
              width: 'auto',
              height: '480px',
              maxHeight: '80vh',
              border: '1px solid #ccc',
              borderRadius: '8px',
              marginTop: '12px',
            }}
          >
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <div className="download-button-wrapper">
            <a href={videoUrl} download target="_blank" rel="noopener noreferrer">
              <button className="download-button">⬇️ Download Video</button>
            </a>
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div className="history-section">
          <h3>Recent Videos</h3>
          <ul>
            {history.map((link, index) => (
              <li key={index}>
                <a href={link} target="_blank" rel="noopener noreferrer">Video {index + 1}</a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
