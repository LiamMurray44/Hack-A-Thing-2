// Written by Claude Code on 2026-01-29
// User prompt: Implement FMLA Deadline & Timeline Tracker Prototype

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Leave Requests API
export const leaveRequestsAPI = {
  getAll: (params = {}) => api.get('/leave-requests/', { params }),
  getById: (id) => api.get(`/leave-requests/${id}`),
  create: (data) => api.post('/leave-requests/', data),
  update: (id, data) => api.patch(`/leave-requests/${id}`, data),
  delete: (id) => api.delete(`/leave-requests/${id}`),
};

// Timeline API
export const timelineAPI = {
  getTimeline: (requestId) => api.get(`/timeline/${requestId}`),
  getCompliance: (requestId) => api.get(`/timeline/${requestId}/compliance`),
  getAllAlerts: () => api.get('/timeline/alerts/all'),
};

// Notifications API
export const notificationsAPI = {
  getAll: (params = {}) => api.get('/notifications/', { params }),
  getByRequestId: (requestId) => api.get(`/notifications/${requestId}`),
  create: (params) => api.post('/notifications/', null, { params }),
  update: (id, readStatus) => api.patch(`/notifications/${id}`, null, {
    params: { read_status: readStatus },
  }),
  delete: (id) => api.delete(`/notifications/${id}`),
};

export default api;
