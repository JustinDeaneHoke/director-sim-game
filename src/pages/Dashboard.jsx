import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getProjects, selectProject } from '../api/api';
import ProjectCard from '../components/ProjectCard';
import { useProject } from '../contexts/ProjectContext';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { setSelectedProject } = useProject();

  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      try {
        const { data } = await getProjects();
        setProjects(data);
      } catch (err) {
        setError('Failed to load projects');
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  const handleSelect = async (project) => {
    try {
      await selectProject(project.id);
      setSelectedProject(project);
      navigate('/project');
    } catch (err) {
      console.error('Error selecting project', err);
    }
  };

  if (loading) return <div className="p-4">Loading projects...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Available Projects</h1>
      {projects.map((proj) => (
        <ProjectCard key={proj.id} project={proj} onSelect={handleSelect} />
      ))}
    </div>
  );
};

export default Dashboard;
