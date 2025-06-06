import React, { useEffect, useState } from 'react';
import ProfileEntry from '../components/ProfileEntry';

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchProfile() {
      try {
        const res = await fetch('/get_profile');
        if (!res.ok) throw new Error('Failed to load profile');
        const data = await res.json();
        setProfile(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchProfile();
  }, []);

  if (loading) return <p>Loading profile...</p>;
  if (error) return <p className="text-red-500">{error}</p>;
  if (!profile) return null;

  const {
    total_projects,
    average_critics_score,
    average_fan_score,
    total_box_office,
    total_viewership,
    awards_won,
    projects = [],
  } = profile;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-4">Career Profile</h1>
      <div className="grid grid-cols-2 gap-4 mb-8 text-sm">
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-gray-600">Total Projects</p>
          <p className="text-xl font-semibold">{total_projects}</p>
        </div>
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-gray-600">Average Critics Score</p>
          <p className="text-xl font-semibold">{average_critics_score}</p>
        </div>
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-gray-600">Average Fan Score</p>
          <p className="text-xl font-semibold">{average_fan_score}</p>
        </div>
        <div className="bg-gray-50 p-4 rounded">
          <p className="text-gray-600">
            {typeof total_viewership === 'number' ? 'Total Viewership' : 'Career Box Office'}
          </p>
          <p className="text-xl font-semibold">
            {typeof total_viewership === 'number'
              ? total_viewership.toLocaleString()
              : `$${(total_box_office || 0).toLocaleString()}`}
          </p>
        </div>
        {awards_won && awards_won.length > 0 && (
          <div className="col-span-2 bg-yellow-50 p-4 rounded">
            <p className="text-yellow-700 font-medium">Awards Won</p>
            <p>{awards_won.join(', ')}</p>
          </div>
        )}
      </div>

      <h2 className="text-xl font-semibold mb-4">Past Projects</h2>
      <div>
        {projects.map((project) => (
          <ProfileEntry key={project.id} project={project} />
        ))}
      </div>
    </div>
  );
}
