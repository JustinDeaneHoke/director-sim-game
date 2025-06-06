import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Results() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function release() {
      try {
        const response = await fetch('/release_project', { method: 'POST' });
        if (!response.ok) {
          throw new Error('Failed to release project');
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    release();
  }, []);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  const {
    critics_score,
    fan_score,
    box_office,
    viewership,
    profit,
    awards,
    flavor_text
  } = data || {};

  const hasAwards = Array.isArray(awards) && awards.length > 0;

  return (
    <div className="container mx-auto p-6 text-white">
      <h1 className="text-3xl font-bold mb-6">Release Results</h1>
      <div className="bg-gray-800 rounded-lg shadow-lg p-6 space-y-4">
        <p className="text-xl">Critics Score: {critics_score}/100</p>
        <p className="text-xl">Audience Score: {fan_score}/100</p>
        {typeof box_office === 'number' ? (
          <p className="text-xl">Box Office: ${box_office.toLocaleString()}</p>
        ) : (
          <p className="text-xl">Viewership: {viewership?.toLocaleString()}</p>
        )}
        <p className="text-xl">Profit: ${profit?.toLocaleString()}</p>

        {hasAwards && (
          <div className="bg-yellow-200 text-yellow-800 rounded-md p-4">
            <h2 className="font-semibold flex items-center mb-2">
              <span className="mr-2">🏆</span> Awards
            </h2>
            <ul className="list-disc ml-5">
              {awards.map((award, idx) => (
                <li key={idx}>{award}</li>
              ))}
            </ul>
          </div>
        )}

        {flavor_text && <p className="italic">{flavor_text}</p>}
        <p className="font-semibold mt-4">
          Your project earned ${profit?.toLocaleString()} and scored a {critics_score} with critics.
        </p>
      </div>
      <button
        onClick={() => navigate('/dashboard')}
        className="mt-6 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
      >
        Return to Dashboard
      </button>
    </div>
  );
}

export default Results;
