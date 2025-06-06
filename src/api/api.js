import axios from 'axios';

const api = axios.create({
  baseURL: '/',
});

export const getProjects = () => api.get('/get_projects');
// Send project ID using the key expected by the backend
export const selectProject = (id) =>
  api.post('/select_project', { project_id: id });

export default api;
