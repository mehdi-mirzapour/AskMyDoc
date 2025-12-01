import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import { uploadFiles, askQuestion, getSchema } from './services/api';
import './App.css';

function App() {
    const [filesUploaded, setFilesUploaded] = useState(false);
    const [uploadStatus, setUploadStatus] = useState(null);

    const handleUploadComplete = async (files) => {
        const response = await uploadFiles(files);
        setUploadStatus(response);
        setFilesUploaded(true);
        return response;
    };

    const handleAskQuestion = async (question) => {
        const response = await askQuestion(question);
        return response;
    };

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

            <div className="main-container">
                {!filesUploaded ? (
                    <div className="upload-section">
                        <h2>Upload Your Excel Files</h2>
                        <FileUpload onUploadComplete={handleUploadComplete} />
                    </div>
                ) : (
                    <div className="chat-section">
                        <ChatInterface onAskQuestion={handleAskQuestion} />
                        <div className="reset-section">
                            <button onClick={() => {
                                setFilesUploaded(false);
                                setUploadStatus(null);
                            }} className="reset-btn">
                                Upload New Files
                            </button>
                        </div>
                    </div>
                )}
            </div>

            <footer className="app-footer">
                <p>Powered by FastAPI + LangChain + LangGraph</p>
            </footer>
        </div>
    );
}

export default App;
