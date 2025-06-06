import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';

const ProjectPage = () => (
  <div className="p-4">Project Page Placeholder</div>
);

const App = () => (
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/project" element={<ProjectPage />} />
  </Routes>
);

export default App;
