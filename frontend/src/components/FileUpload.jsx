import React, { useState } from 'react';

const FileUpload = ({ onUploadComplete }) => {
    const [selectedFiles, setSelectedFiles] = useState([]);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);

    const handleFileChange = (e) => {
        const files = Array.from(e.target.files);
        setSelectedFiles(files);
    };

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const files = Array.from(e.dataTransfer.files);
            setSelectedFiles(files);
        }
    };

    const handleUpload = async () => {
        if (selectedFiles.length === 0) {
            alert('Please select files to upload');
            return;
        }

        setUploading(true);
        try {
            await onUploadComplete(selectedFiles);
            setSelectedFiles([]);
        } catch (error) {
            console.error('Upload error:', error);
            alert('Error uploading files: ' + error.message);
        } finally {
            setUploading(false);
        }
    };

    const removeFile = (index) => {
        setSelectedFiles(files => files.filter((_, i) => i !== index));
    };

    return (
        <div className="file-upload-container">
            <div
                className={`drop-zone ${dragActive ? 'active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    id="fileInput"
                    multiple
                    accept=".xlsx,.xls"
                    onChange={handleFileChange}
                    style={{ opacity: 0, position: 'absolute', zIndex: -1, width: '1px', height: '1px' }}
                />
                <label htmlFor="fileInput" className="file-label">
                    <div className="upload-icon">📁</div>
                    <p>Drag & drop Excel files here or click to browse</p>
                    <p className="hint">Supports .xlsx and .xls files</p>
                </label>
            </div>

            {selectedFiles.length > 0 && (
                <div className="selected-files">
                    <h3>Selected Files ({selectedFiles.length})</h3>
                    <ul>
                        {selectedFiles.map((file, index) => (
                            <li key={index}>
                                <span>📄 {file.name}</span>
                                <button onClick={() => removeFile(index)} className="remove-btn">×</button>
                            </li>
                        ))}
                    </ul>
                    <button
                        onClick={handleUpload}
                        disabled={uploading}
                        className="upload-btn"
                    >
                        {uploading ? 'Uploading...' : 'Upload Files'}
                    </button>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
