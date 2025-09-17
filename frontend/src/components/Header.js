import React from 'react';
import { MessageCircle, Upload, Wifi, WifiOff } from 'lucide-react';

const Header = ({ activeTab, setActiveTab, isConnected }) => {
  return (
    <header className="header">
      <div className="header-content">
        <h1>LLM Agent with Dynamic Knowledge Base</h1>
        
        <nav className="header-nav">
          <button
            className={`nav-button ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <MessageCircle size={18} />
            Chat
          </button>
          <button
            className={`nav-button ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            <Upload size={18} />
            Upload Documents
          </button>
        </nav>
        
        <div className="connection-status">
          {isConnected ? (
            <>
              <Wifi size={16} className="status-dot" />
              <span>Connected</span>
            </>
          ) : (
            <>
              <WifiOff size={16} className="status-dot disconnected" />
              <span>Disconnected</span>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
