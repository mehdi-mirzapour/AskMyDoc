import React, { useState, useRef, useEffect } from 'react';

const ChatInterface = ({ onAskQuestion, onUploadFiles, onResetMemory, hasFiles }) => {
    const [messages, setMessages] = useState([]);
    const [question, setQuestion] = useState('');
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [showSamples, setShowSamples] = useState(false);
    const messagesEndRef = useRef(null);
    const fileInputRef = useRef(null);
    const samplesRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleReset = async () => {
        try {
            await onResetMemory();
            const resetMessage = {
                type: 'system',
                content: '🔄 Agent AI memory reset'
            };
            setMessages(prev => [...prev, resetMessage]);
        } catch (error) {
            console.error('Reset error:', error);
            const errorMessage = {
                type: 'error',
                content: '❌ Failed to reset memory: ' + error.message
            };
            setMessages(prev => [...prev, errorMessage]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        // Check if files are uploaded
        if (!hasFiles) {
            const errorMessage = {
                type: 'system',
                content: '⚠️ Please upload Excel files before asking questions. Click the 📎 button to attach files.'
            };
            setMessages(prev => [...prev, errorMessage]);
            return;
        }

        // Add user message
        const userMessage = { type: 'user', content: question };
        setMessages(prev => [...prev, userMessage]);
        setQuestion('');
        setLoading(true);

        try {
            const response = await onAskQuestion(question);

            // Add AI response
            const aiMessage = {
                type: 'ai',
                content: response.answer,
                sql_queries: response.sql_queries,
                model: response.model
            };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('Question error:', error);
            const errorMessage = {
                type: 'error',
                content: 'Error: ' + error.message
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleFileSelect = async (e) => {
        const files = Array.from(e.target.files);
        if (files.length === 0) return;

        setUploading(true);

        // Add system message about upload
        const uploadingMessage = {
            type: 'system',
            content: `📤 Uploading ${files.length} file(s)...`
        };
        setMessages(prev => [...prev, uploadingMessage]);

        try {
            const response = await onUploadFiles(files);

            // Add success message
            const successMessage = {
                type: 'system',
                content: `✅ Successfully uploaded ${files.length} file(s).Created ${response.tables_created.length} tables with ${response.row_count} rows.You can now ask questions!`
            };
            setMessages(prev => [...prev, successMessage]);
        } catch (error) {
            console.error('Upload error:', error);
            const errorMessage = {
                type: 'error',
                content: '❌ Upload failed: ' + error.message
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setUploading(false);
            // Reset file input
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        }
    };

    const exampleQuestions = [
        "Compute the total revenue per country across all files",
        "Which product has the highest average margin?",
        "Compare sales between Q1 and Q2",
        "List the top 5 customers by total spend"
    ];

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (samplesRef.current && !samplesRef.current.contains(event.target)) {
                setShowSamples(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleExampleClick = (exampleQ) => {
        setQuestion(exampleQ);
        setShowSamples(false);
    };

    return (
        <div className="chat-container">
            <div className="messages-area">
                {messages.length === 0 ? (
                    <div className="welcome-message">
                        <h2>👋 Welcome to AskMyDoc!</h2>
                        <p>Upload your Excel files and start asking questions about your data.</p>
                        <div className="upload-prompt">
                            <p className="upload-hint">📎 Click the attach button below to upload your files</p>
                        </div>
                        <div className="example-questions">
                            <h3>Example questions you can ask:</h3>
                            {exampleQuestions.map((q, i) => (
                                <button
                                    key={i}
                                    onClick={() => handleExampleClick(q)}
                                    className="example-btn"
                                >
                                    {q}
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="messages">
                        {messages.map((msg, index) => (
                            <div key={index} className={`message ${msg.type} `}>
                                <div className="message-icon">
                                    {msg.type === 'user' ? '👤' :
                                        msg.type === 'ai' ? '🤖' :
                                            msg.type === 'system' ? 'ℹ️' : '⚠️'}
                                </div>
                                <div className="message-content">
                                    <p>{msg.content}</p>
                                    {msg.sql_queries && msg.sql_queries.length > 0 && (
                                        <details className="sql-details">
                                            <summary>SQL Queries Used</summary>
                                            {msg.sql_queries.map((query, i) => (
                                                <pre key={i}><code>{query}</code></pre>
                                            ))}
                                        </details>
                                    )}
                                    {msg.model && (
                                        <div className="model-badge">Model: {msg.model}</div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="message ai">
                                <div className="message-icon">🤖</div>
                                <div className="message-content">
                                    <p className="loading">Thinking...</p>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            <form onSubmit={handleSubmit} className="input-area">
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    accept=".xlsx,.xls"
                    multiple
                    style={{ display: 'none' }}
                />
                <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="attach-btn"
                    disabled={uploading}
                    title="Attach Excel files"
                >
                    {uploading ? '⏳' : '📎'}
                </button>

                <div className="samples-container" ref={samplesRef}>
                    <button
                        type="button"
                        onClick={() => setShowSamples(!showSamples)}
                        className="samples-btn"
                        disabled={loading || uploading}
                        title="Sample questions"
                    >
                        💡
                    </button>

                    {showSamples && (
                        <div className="samples-dropdown">
                            <div className="samples-header">Sample Questions</div>
                            {exampleQuestions.map((question, index) => (
                                <button
                                    key={index}
                                    type="button"
                                    onClick={() => handleExampleClick(question)}
                                    className="sample-item"
                                >
                                    {question}
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                <button
                    type="button"
                    onClick={handleReset}
                    className="reset-btn"
                    disabled={loading || uploading}
                    title="Reset Agent Memory"
                >
                    🔄
                </button>

                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder={hasFiles ? "Ask a question about your documents..." : "Upload files first, then ask questions..."}
                    disabled={loading || uploading}
                />
                <button type="submit" disabled={loading || !question.trim() || uploading}>
                    {loading ? '⏳' : '➤'}
                </button>
            </form>
        </div>
    );
};

export default ChatInterface;
