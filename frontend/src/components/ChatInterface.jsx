import React, { useState, useRef, useEffect } from 'react';

const ChatInterface = ({ onAskQuestion }) => {
    const [messages, setMessages] = useState([]);
    const [question, setQuestion] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

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

    const exampleQuestions = [
        "Compute the total revenue per country across all files",
        "Which product has the highest average margin?",
        "Compare sales between Q1 and Q2",
        "List the top 5 customers by total spend",
        "Highlight any missing values or inconsistencies"
    ];

    const handleExampleClick = (exampleQ) => {
        setQuestion(exampleQ);
    };

    return (
        <div className="chat-container">
            <div className="messages-area">
                {messages.length === 0 ? (
                    <div className="welcome-message">
                        <h2>👋 Welcome to AskMyDoc!</h2>
                        <p>Upload your Excel files and start asking questions.</p>
                        <div className="example-questions">
                            <h3>Try these example questions:</h3>
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
                            <div key={index} className={`message ${msg.type}`}>
                                <div className="message-icon">
                                    {msg.type === 'user' ? '👤' : msg.type === 'ai' ? '🤖' : '⚠️'}
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
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question about your documents..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !question.trim()}>
                    {loading ? '⏳' : '➤'}
                </button>
            </form>
        </div>
    );
};

export default ChatInterface;
