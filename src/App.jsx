import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Dashboard, Project, Production, Results, Profile } from './pages';

const App = () => (
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/project" element={<Project />} />
    <Route path="/production" element={<Production />} />
    <Route path="/results" element={<Results />} />
    <Route path="/profile" element={<Profile />} />
  </Routes>
);

export default App;
