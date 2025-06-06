import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CastCard from '../components/CastCard';
import { useProject } from '../contexts/ProjectContext';

function Project() {
  const navigate = useNavigate();
  const { project } = useProject();
  const [talentPools, setTalentPools] = useState({});
  const [selected, setSelected] = useState({});
  const [error, setError] = useState('');

  useEffect(() => {
    if (!project) return;

    async function fetchTalent() {
      const pools = {};
      for (const role of project.roles) {
        try {
          const res = await fetch(`/get_talent_pool?role=${encodeURIComponent(role)}`);
          const data = await res.json();
          pools[role] = data;
        } catch (err) {
          console.error('Failed fetching talent for', role, err);
          pools[role] = [];
        }
      }
      setTalentPools(pools);
    }

    fetchTalent();
  }, [project]);

  const handleSelect = (role, id) => {
    setSelected((prev) => ({ ...prev, [role]: id }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!project) return;
    const missing = project.roles.filter((role) => !selected[role]);
    if (missing.length) {
      setError(`Please select: ${missing.join(', ')}`);
      return;
    }
    try {
      await fetch('/select_cast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selections: selected }),
      });
      navigate('/production');
    } catch (err) {
      console.error('Failed to submit cast', err);
    }
  };

  if (!project) {
    return <p className="p-4">No project selected.</p>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-2">{project.title}</h1>
      <p className="italic mb-4">{project.tagline}</p>
      <div className="mb-4">
        <p>Genre: {project.genre}</p>
        <p>Medium: {project.medium}</p>
        <p>Budget: ${project.budget}</p>
        <p>Attached Talent: {project.attachedTalent || 'None'}</p>
      </div>

      <form onSubmit={handleSubmit}>
        {project.roles.map((role) => (
          <div key={role} className="mb-6">
            <h2 className="text-xl font-semibold mb-2">{role}</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {(talentPools[role] || []).map((talent) => (
                <CastCard
                  key={talent.id}
                  talent={talent}
                  selected={selected[role] === talent.id}
                  onSelect={() => handleSelect(role, talent.id)}
                />
              ))}
            </div>
          </div>
        ))}
        {error && <p className="text-red-600 mb-2">{error}</p>}
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Confirm Cast
        </button>
      </form>
    </div>
  );
}

export default Project;
