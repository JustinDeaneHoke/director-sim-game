import React from 'react';

const ProjectCard = ({ project, onSelect }) => (
  <div className="border rounded p-4 shadow mb-4">
    <h2 className="text-xl font-bold mb-2">{project.title}</h2>
    <p className="italic mb-1">{project.tagline}</p>
    <p className="mb-1">Genre: {project.genre}</p>
    <p className="mb-1">Medium: {project.medium}</p>
    <p className="mb-1">Budget: ${project.budget}</p>
    <p className="mb-1">Risk Level: {project.risk}</p>
    {project.talent && project.talent.length > 0 && (
      <p className="mb-1">Talent: {project.talent.join(', ')}</p>
    )}
    <button
      className="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
      onClick={() => onSelect(project)}
    >
      Select This Project
    </button>
  </div>
);

export default ProjectCard;
