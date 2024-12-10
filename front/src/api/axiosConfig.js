import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:4173', // Base URL for FastAPI backend
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;