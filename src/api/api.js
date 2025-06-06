import axios from 'axios';

const api = axios.create({
  baseURL: '/',
});

export const getProjects = () => api.get('/get_projects');
export const selectProject = (id) => api.post('/select_project', { id });

export default api;
