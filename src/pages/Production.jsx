import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ProductionLog from '../components/ProductionLog';

/**
 * Production page displays live production events and outcomes.
 */
const Production = () => {
  const navigate = useNavigate();
  const [log, setLog] = useState([]);
  const [delays, setDelays] = useState('');
  // Holds a comma separated list of major production issues
  const [issues, setIssues] = useState('');
  const [feedback, setFeedback] = useState('');
  const [qualityScore, setQualityScore] = useState(null);

  useEffect(() => {
    const fetchProduction = async () => {
      try {
        const res = await fetch('/start_production', { method: 'POST' });
        if (!res.ok) throw new Error('Failed to start production');
        const data = await res.json();
        setLog(data.production_notes || []);
        setDelays(data.delays);
        // Convert array of issues to a readable string
        setIssues(Array.isArray(data.issues) ? data.issues.join(', ') : data.issues);
        setFeedback(data.studio_feedback);
        setQualityScore(data.final_quality_score);
      } catch (err) {
        console.error(err);
      }
    };
    fetchProduction();
  }, []);

  const handleFinishProduction = () => {
    navigate('/results');
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold mb-4">Production In Progress</h1>
      {qualityScore !== null && (
        <p className="text-lg">Final Quality Score: {qualityScore}</p>
      )}
      {delays && (
        <div className="bg-yellow-100 text-yellow-800 p-4 rounded">
          <strong>Delays:</strong> {delays}
        </div>
      )}
      {issues && (
        <div className="bg-red-100 text-red-800 p-4 rounded">
          <strong>Major Issues:</strong> {issues}
        </div>
      )}
      <ProductionLog notes={log} />
      {feedback && (
        <div className="bg-gray-100 text-gray-800 p-4 rounded mt-4">
          <strong>Studio Feedback:</strong> {feedback}
        </div>
      )}
      <button
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded"
        onClick={handleFinishProduction}
      >
        Finish Production
      </button>
    </div>
  );
};

export default Production;
