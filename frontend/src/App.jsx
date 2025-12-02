import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import ChatInterface from './components/ChatInterface';
import { uploadFiles, askQuestion, resetMemory } from './services/api';
import './App.css';

function App() {
    const [showChat, setShowChat] = useState(false);
    const [filesUploaded, setFilesUploaded] = useState(false);
    const [uploadStatus, setUploadStatus] = useState(null);

    const handleGetStarted = () => {
        setShowChat(true);
    };

    const handleUploadFiles = async (files) => {
        const response = await uploadFiles(files);
        setUploadStatus(response);
        setFilesUploaded(true);
        return response;
    };

    const handleAskQuestion = async (question) => {
        const response = await askQuestion(question);
        return response;
    };

    const handleResetMemory = async () => {
        const response = await resetMemory();
        return response;
    };

    if (!showChat) {
        return <LandingPage onGetStarted={handleGetStarted} />;
    }

    return (
        <div className="App">
            <header className="app-header">
                <h1>📁 AskMyDoc</h1>
                <p>AI-Powered Document Assistant</p>
                {uploadStatus && (
                    <div className="upload-status">
                        ✓ {uploadStatus.tables_created.length} tables loaded ({uploadStatus.row_count} rows)
                    </div>
                )}
            </header>

            <ChatInterface
                onAskQuestion={handleAskQuestion}
                onUploadFiles={handleUploadFiles}
                onResetMemory={handleResetMemory}
                hasFiles={filesUploaded}
            />

            <footer className="app-footer">
                <p>Powered by FastAPI + LangChain + LangGraph</p>
            </footer>
        </div>
    );
}

export default App;
