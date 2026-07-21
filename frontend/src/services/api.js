// src/services/api.js
// Axios instance wired to the FastAPI backend
import axios from 'axios';

const BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE });

// ── Users ─────────────────────────────────────────────────────────
export const getUsers    = (role) => api.get('/api/users', { params: role ? { role } : {} });
export const getUser     = (id)   => api.get(`/api/users/${id}`);
export const createUser  = (data) => api.post('/api/users', data);
export const updateUser  = (id, data) => api.put(`/api/users/${id}`, data);
export const suspendUser = (id)   => api.post(`/api/users/${id}/suspend`);
export const reactivateUser = (id) => api.post(`/api/users/${id}/reactivate`);
export const deleteUser  = (id)   => api.delete(`/api/users/${id}`);

// ── Projects ──────────────────────────────────────────────────────
export const getProjects      = (params) => api.get('/api/projects', { params });
export const getProject       = (id)     => api.get(`/api/projects/${id}`);
export const createProject    = (data)   => api.post('/api/projects', data);
export const completeProject  = (id, requestor_id) => api.post(`/api/projects/${id}/complete`, { requestor_id });
export const addMember        = (id, data) => api.post(`/api/projects/${id}/members`, data);
export const deleteProject    = (id, requestor_id) => api.delete(`/api/projects/${id}`, { params: { requestor_id } });

// ── Tasks ─────────────────────────────────────────────────────────
export const getTasks    = (params) => api.get('/api/tasks', { params });
export const getTask     = (id)     => api.get(`/api/tasks/${id}`);
export const createTask  = (data)   => api.post('/api/tasks', data);
export const assignTask  = (id, data) => api.post(`/api/tasks/${id}/assign`, data);
export const startTask   = (id, user_id) => api.post(`/api/tasks/${id}/start`, { user_id });
export const completeTask = (id, user_id) => api.post(`/api/tasks/${id}/complete`, { user_id });
export const deleteTask  = (id, requestor_id) => api.delete(`/api/tasks/${id}`, { params: { requestor_id } });

export default api;
