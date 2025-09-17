import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import DocumentUpload from './components/DocumentUpload';
import Header from './components/Header';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check if backend is connected
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await fetch('/health');
      if (response.ok) {
        setIsConnected(true);
      }
    } catch (error) {
      console.error('Backend connection failed:', error);
      setIsConnected(false);
    }
  };

  return (
    <div className="App">
      <Header 
        activeTab={activeTab} 
        setActiveTab={setActiveTab}
        isConnected={isConnected}
      />
      <main className="main-content">
        {activeTab === 'chat' ? (
          <ChatInterface />
        ) : (
          <DocumentUpload onUploadSuccess={checkConnection} />
        )}
      </main>
    </div>
  );
}

export default App;
