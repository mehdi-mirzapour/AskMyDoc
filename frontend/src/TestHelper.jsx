import React from 'react';

// Test helper component to simulate file upload for testing
const TestHelper = ({ onSimulateUpload }) => {
    const simulateUpload = () => {
        const mockResponse = {
            filename: "test_files.xlsx",
            tables_created: ["sales_2023_sales", "sales_2024_sales"],
            row_count: 142,
            status: "success"
        };
        onSimulateUpload(mockResponse);
    };

    return (
        <div style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            zIndex: 9999,
            background: '#ff6b6b',
            padding: '10px 15px',
            borderRadius: '8px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
        }}>
            <button
                onClick={simulateUpload}
                style={{
                    background: 'white',
                    color: '#ff6b6b',
                    border: 'none',
                    padding: '8px 16px',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontWeight: 'bold'
                }}
            >
                🧪 TEST MODE: Simulate Upload
            </button>
        </div>
    );
};

export default TestHelper;
