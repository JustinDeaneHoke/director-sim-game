import axios from 'axios';

const api = axios.create({
  baseURL: '/',
});

export const getProjects = () => api.get('/get_projects');
// Send project ID using the key expected by the backend
export const selectProject = (id) =>
  api.post('/select_project', { project_id: id });

// Start a new game session with a default player name
export const startGame = (name = 'Player') =>
  api.post('/start_game', { name });

export default api;
