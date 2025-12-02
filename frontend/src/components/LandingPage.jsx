import React from 'react';

const LandingPage = ({ onGetStarted }) => {
    return (
        <div className="landing-page">
            <div className="landing-container">
                <div className="hero-section">
                    <div className="hero-content">
                        <h1 className="hero-title">
                            Transform Your <span className="gradient-text">Excel Data</span>
                            <br />
                            into Insights
                        </h1>
                        <p className="hero-description">
                            Upload your Excel files and ask questions in natural language.
                            Our AI-powered assistant analyzes your data and provides instant answers.
                        </p>
                        <button onClick={onGetStarted} className="cta-button">
                            Get Started →
                        </button>

                        <div className="feature-tags">
                            <span className="feature-tag">📊 Excel Analysis</span>
                            <span className="feature-tag">🤖 AI Powered</span>
                            <span className="feature-tag">⚡ Instant Results</span>
                        </div>
                    </div>

                    <div className="hero-visual">
                        <div className="floating-card">
                            <div className="card-header">
                                <div className="card-icon">📁</div>
                                <h3>Your Excel Files</h3>
                            </div>
                            <div className="card-content">
                                <div className="file-item">
                                    <span className="file-emoji">📄</span>
                                    <span>sales_2024.xlsx</span>
                                </div>
                                <div className="file-item">
                                    <span className="file-emoji">📄</span>
                                    <span>inventory.xlsx</span>
                                </div>
                                <div className="file-item">
                                    <span className="file-emoji">📄</span>
                                    <span>customers.xlsx</span>
                                </div>
                            </div>
                            <div className="card-arrow">↓</div>
                            <div className="ai-response">
                                <div className="ai-icon">🤖</div>
                                <p>"Total revenue is $125,333 across all regions"</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="features-section">
                    <div className="feature-card">
                        <div className="feature-icon">🚀</div>
                        <h3>Lightning Fast</h3>
                        <p>Get answers to complex data questions in seconds</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">🔒</div>
                        <h3>Secure & Private</h3>
                        <p>Your data stays private and is never stored</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon">💡</div>
                        <h3>Smart Insights</h3>
                        <p>Powered by advanced AI and natural language processing</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
