import React, { useState } from 'react';
import './App.css';

export default function AppBuilder() {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedFiles, setGeneratedFiles] = useState(null);
  const [activeTab, setActiveTab] = useState('preview');

  const handleGenerate = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Connects to your FastAPI backend
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt })
      });

      const data = await response.json();
      setGeneratedFiles(data.files);
    } catch (error) {
      console.error("Failed to generate:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const getPreviewHtml = () => {
    if (!generatedFiles) return '';

    const html = generatedFiles['index.html'] || '<h1>No HTML generated</h1>';
    const css = generatedFiles['styles.css'] || '';
    const js = generatedFiles['app.js'] || generatedFiles['script.js'] || '';

    return html
      .replace('</head>', `<style>${css}</style></head>`)
      .replace('</body>', `<script>${js}</script></body>`);
  };

  return (
    <div className="app-container">

      {/* LEFT PANEL */}
      <div className="left-panel">
        <h1>AI App Builder</h1>

        <div className="chat-history">
          {isLoading && <p className="loading-text">Agent is writing code...</p>}
        </div>

        <form onSubmit={handleGenerate} className="prompt-form">
          <textarea
            className="prompt-input"
            placeholder="Describe the app you want to build..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <button
            type="submit"
            disabled={isLoading || !prompt}
            className="generate-btn"
          >
            {isLoading ? 'Generating...' : 'Generate App'}
          </button>
        </form>
      </div>

      {/* RIGHT PANEL */}
      <div className="right-panel">
        <div className="tabs">
          <button
            onClick={() => setActiveTab('preview')}
            className={`tab-btn ${activeTab === 'preview' ? 'active' : ''}`}
          >
            Desktop Preview
          </button>
          <button
            onClick={() => setActiveTab('code')}
            className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
          >
            Code
          </button>
        </div>

        <div className="preview-container">
          {!generatedFiles && !isLoading && (
            <p className="placeholder-text">Your app preview will appear here.</p>
          )}

          {generatedFiles && activeTab === 'preview' && (
            <div className="iframe-wrapper">
              <iframe
                title="app-preview"
                srcDoc={getPreviewHtml()}
                sandbox="allow-scripts allow-same-origin"
              />
            </div>
          )}

          {generatedFiles && activeTab === 'code' && (
            <div className="code-wrapper">
               {generatedFiles['index.html']}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}