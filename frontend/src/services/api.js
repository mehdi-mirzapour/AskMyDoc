import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const uploadFiles = async (files) => {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });

    const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

export const askQuestion = async (question) => {
    const response = await axios.post(`${API_BASE_URL}/query/`, {
        question,
    });

    return response.data;
};

export const getSchema = async () => {
    const response = await axios.get(`${API_BASE_URL}/upload/schema`);
    return response.data;
};

export const resetMemory = async () => {
    const response = await axios.post(`${API_BASE_URL}/query/reset`);
    return response.data;
};
