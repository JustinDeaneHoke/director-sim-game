import React from 'react';

/**
 * Display a single past project entry.
 * Poster integration left for future builds.
 */
export default function ProfileEntry({ project }) {
  return (
    <div className="flex items-start space-x-4 py-4 border-b border-gray-200">
      {/* Placeholder for poster image */}
      <div className="w-16 h-24 bg-gray-100 flex-shrink-0" />
      <div className="flex-1">
        <div className="flex justify-between items-baseline">
          <h3 className="text-lg font-semibold">{project.title}</h3>
          {project.year && <span className="text-sm text-gray-500">{project.year}</span>}
        </div>
        <p className="text-sm text-gray-600">{project.medium} &bull; {project.genre}</p>
        <p className="text-sm mt-1">Critics: {project.critics_score} | Fans: {project.fan_score}</p>
        {project.awards && project.awards.length > 0 && (
          <p className="text-sm text-yellow-600 mt-1">Awards: {project.awards.join(', ')}</p>
        )}
      </div>
    </div>
  );
}
